// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Set input variables
username = document.getElementById('username');
useremail = document.getElementById('useremail');
password = document.getElementById('password');
usertype = document.getElementById('usertype');
courses = document.getElementById('courses');

// Get ID
const dataID = sessionStorage.getItem('dataID');

// Select box event listener
usertype.addEventListener('change', function handleChange(event) {
    // Get selected ID
    id = event.target.value;

    // If professor is selected
    if (id == 2) {
        courses.value = 0;
        courses.disabled = false;
    } else {
        courses.value = 0;
        courses.disabled = true;
    }

});

// Get all user types and fill select box
fetch("http://localhost:8080/usertype/all", {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        usertype.innerHTML = '<option value="0">Izaberite...</option>';
        for (var item of result["usertype"]) {
            usertype.innerHTML += '<option value="' + item["id"] + '">' + item["usertype"] + '</option>';
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
        courses.innerHTML = '<option value="0">Izaberite...</option>';
        for (var item of result["courses"]) {
            courses.innerHTML += '<option value="' + item["id"] + '">' + item["coursename"] + '</option>';
        }
    });

// Load data by ID number
fetch("http://localhost:8080/users/" + dataID, {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        username.value = result["name"];
        useremail.value = result["email"];
        usertype.value = result["usertype"];

        // If profesor is selected
        if (result["usertype"] == 2) {
            courses.disabled = false;

            // Get profesor course data
            fetch("http://localhost:8080/profesorscourses/profesor/" + dataID, {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
            })
                .then((response) => response.json())
                .then((result) => {
                    courses.value = result["courseid"];
                });
        } else {
            courses.value = 0;
            courses.disabled = true;
        }
    });

// Save data click
document.getElementById('savedata').onclick = function (e) {
    e.preventDefault();

    // Check if fields are filled
    if (username.value == '' || useremail.value == '' || usertype.value == "0") {
        msg.classList.remove('d-none');
        msg.innerHTML = 'Niste popunili potrebna polja';
        return;
    }
    if (usertype.value == "2" && courses.value == "0") {
        msg.classList.remove('d-none');
        msg.innerHTML = 'Niste popunili potrebna polja';
        return;
    }

    // If fields are filled
    if (username.value != '' && useremail.value != '' && usertype.value != "0") {
        // Update user type
        fetch('http://localhost:8080/users/update/' + dataID, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                name: username.value,
                email: useremail.value,
                usertype: usertype.value,
                password: password.value
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if (result['msg']) {
                    // Error savig data
                    msg.classList.remove('d-none');
                    msg.innerHTML = result['msg'];
                } else {
                    // If usertype is profesor
                    if (usertype.value == "2") {
                        fetch('http://localhost:8080/profesorscourses/updatebyprofessor/' + dataID, {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            body: JSON.stringify({
                                courseid: courses.value
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
                                    msg.innerHTML = 'Podaci su uspješno snimljeni. Pričekajte na redirekciju...';
                                    sessionStorage.removeItem('dataID');

                                    // Dummy wait
                                    setTimeout(() => {
                                        // Remove alert box
                                        msg.classList.add('d-none');

                                        // Clear inputs
                                        document.getElementById("forma").reset();

                                        // Redirect page
                                        window.location.href = "/users/list.html";
                                    }, "2000");
                                }
                            });
                    } else {
                        // Successful save
                        msg.classList.remove('alert-danger', 'd-none');
                        msg.classList.add('alert-success');
                        msg.innerHTML = 'Podaci su uspješno snimljeni. Pričekajte na redirekciju...';
                        sessionStorage.removeItem('dataID');

                        // Dummy wait
                        setTimeout(() => {
                            // Remove alert box
                            msg.classList.add('d-none');

                            // Clear inputs
                            document.getElementById("forma").reset();

                            // Redirect page
                            window.location.href = "/users/list.html";
                        }, "2000");
                    }
                }
            });
    }
}

// Cancel save
document.getElementById('cancelsave').onclick = function (e) {
    e.preventDefault();

    // Remove alert box
    msg.classList.add('d-none');

    // Clear inputs
    document.getElementById("forma").reset();
    sessionStorage.removeItem('dataID');

    // Redirect page
    window.location.href = "/users/list.html";
}