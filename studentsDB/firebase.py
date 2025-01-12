import firebase_admin

from firebase_admin import credentials, auth # type: ignore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\Users\anand\PycharmProjects\Interview_website\student-management-fb0ce-firebase-adminsdk-3n618-a3eb6c0593.json")
firebase_admin.initialize_app(cred)
