// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Set input variables
coursename = document.getElementById('coursename');
description = document.getElementById('description');

// Get ID
const dataID = sessionStorage.getItem('dataID');

// Load data by ID number
fetch("http://localhost:8080/courses/" + dataID, {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        coursename.value = result["coursename"];
        description.value = result["description"];
    });

// Save data click
document.getElementById('savedata').onclick = function (e) {
    e.preventDefault();

     // Check if fields are filled
     if (coursename.value == '' || description.value == '') {
        msg.classList.remove('d-none');
        msg.innerHTML = 'Niste popunili potrebna polja';
        return;
    }

    // If typename is filled
    if (coursename.value != '' && description.value != '') {
        // Update course
        fetch('http://localhost:8080/courses/update/' + dataID, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                coursename: coursename.value,
                description: description.value,
                link: 'course.html'
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
                        window.location.href = "/courses/list.html";
                    }, "2000");
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
    window.location.href = "/courses/list.html";
}