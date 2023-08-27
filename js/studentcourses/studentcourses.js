// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Define variables and constants
const sbstudent = document.getElementById('student');
studentscourseslist = {};
createupdatestatus = "add";
studentcourseid = 0;

// Select box event listener
sbstudent.addEventListener('change', function handleChange(event) {
    // Get selected ID
    id = event.target.value;

    // Define select box
    courses = document.getElementById('courses');

    // Clear list
    list = document.getElementById("list");
    list.innerHTML = "";

    // If students is selected
    if (id != 0) {
        // Enable courses selected box
        courses.value = 0;
        courses.disabled = false;

        // Get all student courses and fill the table
        fetch("http://localhost:8080/studentscourses/student/" + id, {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
        })
            .then((response) => response.json())
            .then((result) => {
                studentscourseslist = result;
                for (var item of result["studentscourses"]) {
                    list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td>' + item["name"] + '</td><td>' + item["coursename"] + '</td><td>' + item["grade"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnUpdate(' + item["id"] + ')">Ažuriraj</button><button class="btn btn-danger btn-sm" onclick="fnRemove(' + item["id"] + ')">Ukloni</button></td></tr>';
                }
            });
    } else {
        courses.value = 0;
        courses.disabled = true;
    }
});

// Get all students and fill select box
fetch("http://localhost:8080/users/typeid/1", {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        sbstudent.innerHTML = '<option value="0" selected>Izaberite...</option>';
        for (var item of result["users"]) {
            student.innerHTML += '<option value="' + item["id"] + '">' + item["name"] + '</option>';
        }
    });

// Get all courses and fill select box
fetch("http://localhost:8080/courses/all", {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        courses = document.getElementById("courses");
        courses.innerHTML = '<option value="0" selected>Izaberite...</option>';
        for (var item of result["courses"]) {
            courses.innerHTML += '<option value="' + item["id"] + '">' + item["coursename"] + '</option>';
        }
    });

// Add course to student
document.getElementById('addcourse').onclick = function (e) {
    e.preventDefault();

    // Set input variables
    student = document.getElementById('student');
    courses = document.getElementById('courses');
    grade = document.getElementById('grade');

    // Check if fields are selected nad inserted
    if (student.value == '0' || courses.value == '0' || grade.value == '') {
        msg.classList.remove('d-none');
        msg.innerHTML = 'Niste izabrali ili upisali potrebna polja';
        return;
    }

    // Check if course is already added to student
    if (createupdatestatus == "add") {
        for (var item of studentscourseslist["studentscourses"]) {
            if (courses.value == item["courseid"]) {
                msg.classList.remove('d-none');
                msg.classList.add('alert-danger');
                msg.innerHTML = 'Izabrani predmet je već dodjeljen studentu';
                return;
            }
        }
    }

    // If fields are filled and selected
    if (student.value != '0' || courses.value != '0' || grade.value != '') {
        // set endpoint
        endpoint = ((createupdatestatus == "add") ? 'http://localhost:8080/studentscourses/create' : 'http://localhost:8080/studentscourses/update/' + studentcourseid);

        // Create user
        fetch(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                studentid: student.value,
                courseid: courses.value,
                grade: grade.value
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if (result['msg']) {
                    // Error savig data
                    msg.classList.remove('d-none');
                    msg.innerHTML = result['msg'];
                } else {
                    // Successful save
                    msg.classList.remove('alert-danger', 'd-none');
                    msg.classList.add('alert-success');
                    msg.innerHTML = 'Podaci su uspješno snimljeni.';

                    // Clear input of course and grade
                    courses.value = 0;
                    grade.value = "";

                    // Reste variables and inputs if update is performed
                    if (createupdatestatus != "add") {
                        createupdatestatus = "add";
                        document.getElementById('addcourse').innerHTML = "Dodaj predmet"
                        document.getElementById('cancelupdate').classList.add('d-none');

                        // Enable inputs for update
                        student.disabled = false;
                        courses.disabled = false;
                    }

                    // Get all student courses and fill the table
                    fetch("http://localhost:8080/studentscourses/student/" + student.value, {
                        method: "GET",
                        headers: {
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                    })
                        .then((response) => response.json())
                        .then((result) => {
                            studentscourseslist = result;
                            list = document.getElementById("list");
                            list.innerHTML = "";
                            for (var item of result["studentscourses"]) {
                                list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td>' + item["name"] + '</td><td>' + item["coursename"] + '</td><td>' + item["grade"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnUpdate(' + item["id"] + ')">Ažuriraj</button><button class="btn btn-danger btn-sm" onclick="fnRemove(' + item["id"] + ')">Ukloni</button></td></tr>';
                            }
                        });

                    // Dummy wait
                    setTimeout(() => {
                        // Remove alert box
                        msg.classList.add('d-none');
                    }, "2000");
                }
            });
    }
}

// Function for data update
function fnUpdate(id) {
    // Set input variables
    student = document.getElementById('student');
    courses = document.getElementById('courses');
    grade = document.getElementById('grade');

    // Disable inputs for update
    student.disabled = true;
    courses.disabled = true;

    // Get course info
    fetch("http://localhost:8080/studentscourses/" + id, {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((result) => {
            courses.value = result["courseid"];
            grade.value = result["grade"];
            createupdatestatus = "update";
            studentcourseid = id;
            document.getElementById('addcourse').innerHTML = "Ažuriraj predmet"
            document.getElementById('cancelupdate').classList.remove('d-none');
        });
}

// Cancel course update
document.getElementById('cancelupdate').onclick = function (e) {
    e.preventDefault();

    // Set input variables
    student = document.getElementById('student');
    courses = document.getElementById('courses');
    grade = document.getElementById('grade');

    createupdatestatus = "add";
    document.getElementById('addcourse').innerHTML = "Dodaj predmet"
    document.getElementById('cancelupdate').classList.add('d-none');

    // Set input variables
    courses.value = 0;
    grade.value = "";

    // Enable inputs for update
    student.disabled = false;
    courses.disabled = false;
}

function fnRemove(id) {
    // Set data id into session storage
    sessionStorage.setItem('dataID', id);

    // Open modal window
    modal = document.getElementById("confirmRemove");
    modal.style.display = "block";
}

// Click on No button in modal window
live("click", "btnNo", function (event) {
    // Remove data id from session storage
    sessionStorage.removeItem('dataID');

    // Close modal window
    modal = document.getElementById("confirmRemove");
    modal.style.display = "none";
});

// Click on Yes button in modal window
live("click", "btnYes", function (event) {
    // Get data id from session storage
    dataID = sessionStorage.getItem('dataID');

    // Set input variables
    student = document.getElementById('student');
    courses = document.getElementById('courses');
    grade = document.getElementById('grade');

    // Delete data from database and refresh list
    fetch('http://localhost:8080/studentscourses/delete/' + dataID, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((result) => {
            if (result['msg']) {
                // Error deleting data
                msg.classList.remove('d-none');
                msg.innerHTML = result['msg'];
            } else {
                // Successful deletation
                // Clear input of course and grade
                courses.value = 0;
                grade.value = "";

                // Get all student courses and fill the table
                fetch("http://localhost:8080/studentscourses/student/" + student.value, {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                })
                    .then((response) => response.json())
                    .then((result) => {
                        studentscourseslist = result;
                        list = document.getElementById("list");
                        list.innerHTML = "";
                        for (var item of result["studentscourses"]) {
                            list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td>' + item["name"] + '</td><td>' + item["coursename"] + '</td><td>' + item["grade"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnUpdate(' + item["id"] + ')">Ažuriraj</button><button class="btn btn-danger btn-sm" onclick="fnRemove(' + item["id"] + ')">Ukloni</button></td></tr>';
                        }
                    });
            }
        });

    // Set data id into session storage
    sessionStorage.removeItem('dataID');

    // Close modal window
    modal = document.getElementById("confirmRemove");
    modal.style.display = "none";
});