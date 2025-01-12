import app from "./firebase-config";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const auth = getAuth(app);

document.getElementById("login-form").addEventListener("submit", function (event) {
    event.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    auth.signInWithEmailAndPassword(email, password)
      .then((userCredential) => {
        console.log("User logged in:", userCredential.user);
        alert("Login successful!");
  
        // Get Firebase ID Token
        userCredential.user.getIdToken().then((idToken) => {
          // Send ID token to backend
          fetch('/login/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id_token: idToken }),
          })
          .then(response => response.json())
          .then(data => {
            console.log("Backend response:", data);
            window.location.href = "/dashboard/"; // Redirect to dashboard
          })
          .catch((error) => {
            console.error("Error during backend login:", error);
          });
        });
      })
      .catch((error) => {
        console.error("Error logging in:", error.code, error.message);
        alert(error.message);
      });
  });
  
