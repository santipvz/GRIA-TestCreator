/* assets/js/themeToggle.js */

function toggleTheme() {
    const themeLink = document.getElementById("theme-link");

    // Cambiar de dark a light
    if (themeLink.getAttribute("href").includes("dark.css")) {
        themeLink.href = "assets/css/style.css";
        localStorage.setItem("theme", "light");
    } else {
        // De light a dark
        themeLink.href = "assets/css/dark.css";
        localStorage.setItem("theme", "dark");
    }
}

// Al cargar la página, restaurar el tema previo
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    const themeLink = document.getElementById("theme-link");

    if (savedTheme === "dark") {
        themeLink.href = "assets/css/dark.css";
    } else {
        themeLink.href = "assets/css/style.css";
    }
});
