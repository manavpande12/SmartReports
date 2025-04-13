
document.addEventListener("DOMContentLoaded", function () {
    let menuIcon = document.getElementById("menu-icon");
    let sidebar = document.getElementById("sidebar");
    let closeIcon = document.getElementById("cross-icon");

    

    // Open Sidebar
    menuIcon.addEventListener("click", function () {
        sidebar.classList.add("active");
    });

    // Close Sidebar
    closeIcon.addEventListener("click", function () {
        sidebar.classList.remove("active");
    });

    //Hide Logo
    let logo = document.querySelector(".navbar img");

    if (window.innerWidth <= 522) {
        logo.classList.add("remove");
    }
});


window.addEventListener("resize", function () {
    let logo = document.querySelector(".navbar img");

    if (window.innerWidth <= 522) {
        logo.classList.add("remove"); // Hide when <= 522px
    } else {
        logo.classList.remove("remove"); // Show when > 522px
    }
});








