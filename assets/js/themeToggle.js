// assets/js/themeToggle.js

// Definición del SVG para el ícono de sol (modo claro)
const sunSvg = `<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor">
  <path d="M6.76 4.84l-1.8-1.79L3.17 5.84l1.79 1.79 1.8-1.79zM1 13h3v-2H1v2zm10-9h-2v3h2V4zm7.83 1.83l-1.79-1.79-1.42 1.42 1.79 1.79 1.42-1.42zM17 13v-2h3v2h-3zm-5 7c-2.76 0-5-2.24-5-5 0-2.76 2.24-5 5-5s5 2.24 5 5c0 2.76-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3 0 1.65 1.34 3 3 3s3-1.35 3-3c0-1.66-1.34-3-3-3zm5.24 3.76l1.79 1.79 1.42-1.42-1.79-1.79-1.42 1.42zM4.24 17.16l1.79 1.79 1.42-1.42-1.79-1.79-1.42 1.42zM13 20h-2v3h2v-3z"/>
</svg>`;

// Definición del SVG para el ícono de luna (modo oscuro)
const moonSvg = `<svg viewBox="0 0 24 24" width="32" height="32" fill="currentColor">
  <path d="M21.75 15.06c-1.04.47-2.15.75-3.3.75-4.42 0-8-3.58-8-8 0-1.15.28-2.26.75-3.3.17-.38-.16-.75-.57-.65-3.66.82-6.45 3.92-6.45 7.25 0 4.14 3.36 7.5 7.5 7.5 3.33 0 6.43-2.79 7.25-6.45.1-.41-.27-.74-.65-.57z"/>
</svg>`;

function toggleTheme() {
    const themeLink = document.getElementById("theme-link");
    const themeIconContainer = document.getElementById("theme-icon");

    // Si se está usando la hoja de estilos oscura, cambiar a claro
    if (themeLink.getAttribute("href").includes("dark.css")) {
        themeLink.href = "assets/css/style.css";
        localStorage.setItem("theme", "light");
        themeIconContainer.innerHTML = sunSvg;
    } else {
        // De lo contrario, cambiar a modo oscuro
        themeLink.href = "assets/css/dark.css";
        localStorage.setItem("theme", "dark");
        themeIconContainer.innerHTML = moonSvg;
    }
}

// Al cargar la página, establecer el tema y el ícono según la preferencia almacenada
document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    const themeLink = document.getElementById("theme-link");
    const themeIconContainer = document.getElementById("theme-icon");

    if (savedTheme) {
        if (savedTheme === "dark") {
            themeLink.href = "assets/css/dark.css";
            themeIconContainer.innerHTML = moonSvg;
        } else {
            themeLink.href = "assets/css/style.css";
            themeIconContainer.innerHTML = sunSvg;
        }
    } else {
        // Valor por defecto: modo claro
        themeLink.href = "assets/css/style.css";
        themeIconContainer.innerHTML = sunSvg;
    }
});
