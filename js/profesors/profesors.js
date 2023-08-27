// Get user data
user = JSON.parse(sessionStorage.user);
document.getElementById("name").innerHTML = user["name"];

// Get course name
fetch("http://localhost:8080/profesorscourses/profesor/" + user["id"], {
    method: "GET",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})
    .then((response) => response.json())
    .then((result) => {
        document.getElementById("course").innerHTML = result["coursename"];

        // Get and set students attendence
        fetch("http://localhost:8080/courseapplication/hour/" + result["courseid"], {
            method: "GET",
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
        })
            .then((response) => response.json())
            .then((result) => {
                list = document.getElementById("list");
                i = 1;
                for (var item of result["courseapplication"]) {
                    list.innerHTML += '<tr><th scope="row">' + i + '</th><td>' + item["name"] + '</td><td>' + item["email"] + '</td><td>' + item["logindate"] + '</td></tr>';
                    i++;
                }
            });
    });

