// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Get all student courses
fetch("http://localhost:8080/studentscourses/student/" + user["id"], {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        list = document.getElementById("list");
        for (var item of result["studentscourses"]) {
            list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td><a href=\"javascript:fnShowCourse(\'' + item["link"] + '\', ' + item["courseid"] + ');\">' + item["coursename"] + '</td><td>' + item["description"] + '</td><td>' + item["grade"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnStartClass(' + item["studentid"] + ', ' + item["courseid"] + ')">Prijava na predmet</button></td></tr>';
        }
    });

// Show course details
function fnShowCourse(link, courseid) {
    sessionStorage.setItem('courseid', courseid);
    window.location.href = link;
}

// 
// Function for data update
function fnStartClass(studentid, courseid) {
    // Modal window
    modal = document.getElementById("confirmApplication");
    modalbody = document.getElementById("modalbody");
    confirmApplicationTitle = document.getElementById("confirmApplicationTitle");

    // Start application
    fetch('http://localhost:8080/courseapplication/app', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            userid: studentid,
            courseid: courseid
        }),
    })
        .then((response) => response.json())
        .then((result) => {
            if (result['msg']) {
                // Error
                confirmApplicationTitle.innerHTML = "Greška prilikom prijave na predmet";
                modalbody.innerHTML = result["msg"];
                modal.style.display = "block";
            } else {
                // Successful course application
                confirmApplicationTitle.innerHTML = "Prijava na predmet";
                modalbody.innerHTML = "Uspješna prijava na predmet";
                modal.style.display = "block";
            }
        });    
}

// Click on OK button in modal window
live("click", "btnOK", function (event) {
    // Close modal window
    modal = document.getElementById("confirmApplication");
    modal.style.display = "none";
});