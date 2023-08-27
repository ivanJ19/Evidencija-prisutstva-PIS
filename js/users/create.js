// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Define variables and constants
const sbusertype = document.getElementById('usertype');

// Select box event listener
sbusertype.addEventListener('change', function handleChange(event) {
    // Get selected ID
    id = event.target.value;

    // Define select box
    courses = document.getElementById('courses');

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
        usertype = document.getElementById("usertype");
        usertype.innerHTML = '<option value="0" selected>Izaberite...</option>';
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
        courses = document.getElementById("courses");
        courses.innerHTML = '<option value="0" selected>Izaberite...</option>';
        for (var item of result["courses"]) {
            courses.innerHTML += '<option value="' + item["id"] + '">' + item["coursename"] + '</option>';
        }
    });

// Save data click
document.getElementById('savedata').onclick = function (e) {
    e.preventDefault();

    // Set input variables
    username = document.getElementById('username');
    useremail = document.getElementById('useremail');
    password = document.getElementById('password');
    usertype = document.getElementById('usertype');
    courses = document.getElementById('courses');

    // Check if fields are filled
    if (username.value == '' || useremail.value == '' || usertype.value == "0" || password.value == '') {
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
    if (username.value != '' && useremail.value != '' && usertype.value != "0" && password.value != '') {
        // Create user
        fetch('http://localhost:8080/users/create', {
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
                        // Create user
                        fetch('http://localhost:8080/profesorscourses/create', {
                            method: 'PUT',
                            headers: {
                                'Content-Type': 'application/json',
                                'Accept': 'application/json'
                            },
                            body: JSON.stringify({
                                profesorid: result['id'],
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

    // Redirect page
    window.location.href = "/users/list.html";
}