import { initializeApp } from "firebase/app";

// Firebase Configuration
const firebaseConfig = {
apiKey: "AIzaSyBm7v60zO6jR06wRrOVP-2XKPgaTI4ptho",
authDomain: "student-management-fb0ce.firebaseapp.com",
projectId: "student-management-fb0ce",
storageBucket: "student-management-fb0ce.firebasestorage.app",
messagingSenderId: "31376910002",
appId: "1:31376910002:web:f2a0209972474246020bab",
measurementId: "G-32KJBDF8JJ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = firebase.auth();
