auth.onAuthStateChanged(function (user) {
    if (user) {
      console.log("User is signed in:", user);
      // Example: Hide the login/signup links, show the dashboard link
      document.getElementById("user-status").innerText = `Welcome, ${user.email}`;
    } else {
      console.log("No user is signed in.");
      // Redirect to login page if not authenticated
      window.location.href = "/login/";
    }
  });
  