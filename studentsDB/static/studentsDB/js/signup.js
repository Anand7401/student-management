document.getElementById("signup-form").addEventListener("submit", function (event) {
    event.preventDefault();
  
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
  
    auth.createUserWithEmailAndPassword(email, password)
      .then((userCredential) => {
        console.log("User created:", userCredential.user);
        alert("Signup successful!");
        window.location.href = "/login/"; // Redirect to login page after signup
      })
      .catch((error) => {
        console.error("Error signing up:", error.code, error.message);
        alert(error.message);
      });
  });
  