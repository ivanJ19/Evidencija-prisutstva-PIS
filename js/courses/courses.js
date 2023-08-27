// Get user and course data
user = JSON.parse(sessionStorage.user);
courseid = sessionStorage.courseid

// Set user name
document.getElementById("name").innerHTML = user["name"];

// Get course data
fetch("http://localhost:8080/studentscourses/course/" + user["id"] + "/" + courseid, {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        document.getElementById("list").innerHTML = '<tr><td scope="row">' + result["coursename"] + '</td><td>' + result["description"] + '</td><td>' + result["grade"] + '</td></tr>'
    });