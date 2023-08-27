// Logout
document.getElementById("logout").onclick = function (e) {
    e.preventDefault();

    // Clear session keys and redirect to login
    sessionStorage.removeItem("user");
    sessionStorage.removeItem("courseid");
    window.location.href = "/";
}

// Home
document.getElementById("home").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/students.html";
}