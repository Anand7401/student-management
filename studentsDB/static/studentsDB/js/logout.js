document.getElementById("logout-btn").addEventListener("click", function () {
    auth.signOut()
      .then(() => {
        console.log("User signed out");
        alert("Logout successful!");
        window.location.href = "/login/"; // Redirect to login page
      })
      .catch((error) => {
        console.error("Error signing out:", error.message);
        alert(error.message);
      });
  });
  
