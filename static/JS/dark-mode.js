
document.addEventListener("DOMContentLoaded", function () {
    let modeBtn = document.getElementById("mode-toggle");
    let modeIcon = document.getElementById("mode-icon");
    let modeText = document.getElementById("mode-text");

    // Select specific sections to apply dark mode
    let sections = document.querySelectorAll(".dark-section"); // Use this class on all sections that need dark mode

    if (!modeBtn || !modeIcon || !modeText) {
        console.error("Dark mode elements not found.");
        return;
    }

    // Apply dark mode from localStorage
    if (localStorage.getItem("darkMode") === "enabled") {
        sections.forEach(section => section.classList.add("dark-mode"));
        modeIcon.classList.replace("fa-moon", "fa-sun");
        modeText.textContent = "Light Mode";
    }

    // Toggle dark mode for specific sections
    modeBtn.addEventListener("click", function () {
        let isDarkMode = localStorage.getItem("darkMode") === "enabled";

        if (isDarkMode) {
            sections.forEach(section => section.classList.remove("dark-mode"));
            localStorage.setItem("darkMode", "disabled");
            modeIcon.classList.replace("fa-sun", "fa-moon");
            modeText.textContent = "Dark Mode";
        } else {
            sections.forEach(section => section.classList.add("dark-mode"));
            localStorage.setItem("darkMode", "enabled");
            modeIcon.classList.replace("fa-moon", "fa-sun");
            modeText.textContent = "Light Mode";
        }
    });
});
