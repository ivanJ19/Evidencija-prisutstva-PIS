// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Get all user types
fetch("http://localhost:8080/users/all", {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    },
})
    .then((response) => response.json())
    .then((result) => {
        list = document.getElementById("list");
        for (var item of result["users"]) {
            list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td>' + item["name"] + '</td><td>' + item["email"] + '</td><td>' + item["typename"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnUpdate(' + item["id"] + ')">Ažuriraj</button>' + ((item["id"] > 1) ? '<button class="btn btn-danger btn-sm" onclick="fnDelete(' + item["id"] + ')">Obriši</button>' : "") + '</td></tr>';
        }
    });

// Function for data update
function fnUpdate(id) {
    // Set data id into session storage
    sessionStorage.setItem('dataID', id);

    // Redirect page
    window.location.href = "/users/update.html";
}

function fnDelete(id) {
    // Set data id into session storage
    sessionStorage.setItem('dataID', id);

    // Open modal window
    modal = document.getElementById("confirmDelete");
    modal.style.display = "block";
}

// Click on No button in modal window
live("click", "btnNo", function (event) {
    // Remove data id from session storage
    sessionStorage.removeItem('dataID');

    // Close modal window
    modal = document.getElementById("confirmDelete");
    modal.style.display = "none";
});

// Click on Yes button in modal window
live("click", "btnYes", function (event) {
    // Get data id from session storage
    dataID = sessionStorage.getItem('dataID');

    // Delete data from database and refresh list
    fetch('http://localhost:8080/users/delete/' + dataID, {
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
                // Get all user types
                fetch("http://localhost:8080/users/all", {
                    method: "GET",
                    headers: {
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                })
                    .then((response) => response.json())
                    .then((result) => {
                        list = document.getElementById("list");
                        list.innerHTML = "";
                        for (var item of result["users"]) {
                            list.innerHTML += '<tr><td scope="row">' + item["id"] + '</td><td>' + item["name"] + '</td><td>' + item["email"] + '</td><td>' + item["typename"] + '</td><td><button class="btn btn-success btn-sm btn-action" onclick="fnUpdate(' + item["id"] + ')">Ažuriraj</button>' + ((item["id"] > 1) ? '<button class="btn btn-danger btn-sm" onclick="fnDelete(' + item["id"] + ')">Obriši</button>' : "") + '</td></tr>';
                        }
                    });
            }
        });

    // Set data id into session storage
    sessionStorage.removeItem('dataID');

    // Close modal window
    modal = document.getElementById("confirmDelete");
    modal.style.display = "none";    
});