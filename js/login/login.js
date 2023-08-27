// Login click
document.getElementById('login').onclick = function (e) {
    e.preventDefault();

    // Set input variables
    email = document.getElementById('email');
    password = document.getElementById('password');
    msg = document.getElementById('msg');

    // Check if email and password are filled
    if (email.value == '' || password.value == '') {        
        msg.classList.remove('d-none');
        msg.innerHTML = 'Niste popunili potrebna polja';
    }

    // If email and password are filled
    if (email.value != '' && password.value != '') {
        // Get login data
        fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                email: email.value,
                password: password.value
            }),
        })
            .then((response) => response.json())
            .then((result) => {
                if (result['msg']) {
                    // Wrong email or password
                    msg.classList.remove('d-none');
                    msg.innerHTML = result['msg'];
                } else {
                    // Successful login
                    msg.classList.remove('alert-danger', 'd-none');
                    msg.classList.add('alert-success');
                    msg.innerHTML = 'Uspješna prijava. Pričekajte na redirekciju...';
                    sessionStorage.setItem('user', JSON.stringify(result));                    

                    // Dummy wait
                    setTimeout(() => {
                        // Remove alert box
                        msg.classList.add('d-none');

                        // Clear inputs
                        document.getElementById("forma").reset();

                        // Redirect page
                        if (result['usertype'] == 1) {
                            window.location.href = 'students.html';
                        } else {
                            window.location.href = 'profesors.html';
                        }
                    }, "2000");
                }
            });
    }
}