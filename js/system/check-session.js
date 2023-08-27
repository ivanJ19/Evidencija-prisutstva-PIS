// Redirect to login if session key not exists
if (!sessionStorage.user) {
    window.location.href = "/";
}