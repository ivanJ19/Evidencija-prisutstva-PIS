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

    window.location.href = "/profesors.html";
}

// Create user type
document.getElementById("createusertype").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/usertype/create.html";
}

// List user types
document.getElementById("usertypelist").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/usertype/list.html";
}

// Create user
document.getElementById("createuser").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/users/create.html";
}

// List users
document.getElementById("userlist").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/users/list.html";
}

// Create courses
document.getElementById("createcourse").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/courses/create.html";
}

// List courses
document.getElementById("courselist").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/courses/list.html";
}

// List courses
document.getElementById("connstudentcourse").onclick = function (e) {
    e.preventDefault();

    window.location.href = "/studentcourses/studentcourses.html";
}
