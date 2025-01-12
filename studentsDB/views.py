import os

import requests
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db import models
from django.contrib import messages
import csv

# Create your views here.

from .models import Student
from .forms import StudentForm

from django.http import JsonResponse
from firebase_admin import auth
import json

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Create a new user in Firebase
            user = auth.create_user(
                email=email,
                password=password,
            )
            return JsonResponse({"message": "User created successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "studentsDB/signup.html")
from django.http import JsonResponse
from firebase_admin import auth
from django.contrib.sessions.backends.db import SessionStore

FIREBASE_WEB_API_KEY = os.getenv('FIREBASE_WEB_API_KEY')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Use Firebase REST API to authenticate the user
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                # Create a session for the authenticated user
                session = SessionStore()
                session['uid'] = data['localId']  # Firebase User ID
                session.save()

                # Save the session ID in a cookie
                request.session['uid'] = data['localId']

                return redirect('student_list')
            else:
                error_message = data.get("error", {}).get("message", "Invalid email or password.")
                return render(request, 'studentsDB/login.html', {"error": error_message})
        except Exception as e:
            return render(request, 'studentsDB/login.html', {"error": "An error occurred during login."})

    return render(request, 'studentsDB/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def student_list(request):
    if 'uid' not in request.session:
        return redirect('login')

    students = Student.objects.all()
    query = request.GET.get('query', '')
    sort_by = request.GET.get('sort_by', 'id')

    if query:
        students = students.filter(name__icontains=query)

    students = students.order_by(sort_by)

    context = {
        'students': students,
    }
    return render(request, 'studentsDB/student_list.html', context)

def add_student(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'studentsDB/add_student.html', {'form': form})

def edit_student(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'studentsDB/edit_student.html', {'form': form})

def delete_student(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    student = Student.objects.get(pk=pk)
    student.delete()
    return redirect('student_list')

def export_students(request):
    students = Student.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Age', 'Email', 'Address'])
    for student in students:
        writer.writerow([student.id, student.name, student.age, student.email, student.address])

    return response