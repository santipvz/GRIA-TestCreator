// assets/js/themeToggle.js
function toggleTheme() {
    const themeLink = document.getElementById("theme-link");
    const themeIcon = document.getElementById("theme-icon");

    // Si se está usando el modo oscuro, cambiamos a claro
    if (themeLink.getAttribute("href").includes("dark.css")) {
        themeLink.href = "assets/css/style.css";
        localStorage.setItem("theme", "light");
        // Cambiamos el icono a sol (modo claro)
        themeIcon.src = "assets/images/sun.png";
    } else {
        // Sino, cambiamos a modo oscuro
        themeLink.href = "assets/css/dark.css";
        localStorage.setItem("theme", "dark");
        // Cambiamos el icono a luna (modo oscuro)
        themeIcon.src = "assets/images/sun.png";
    }
}

// Para mantener la preferencia de tema al recargar la página:
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    const themeLink = document.getElementById("theme-link");
    const themeIcon = document.getElementById("theme-icon");
    if (savedTheme) {
        if (savedTheme === "dark") {
            themeLink.href = "assets/css/dark.css";
            themeIcon.src = "assets/images/sun.png";
        } else {
            themeLink.href = "assets/css/style.css";
            themeIcon.src = "assets/images/sun.png";
        }
    }
});
