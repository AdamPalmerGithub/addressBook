function choice(ch) {
    localStorage.setItem('theme', ch);
    applyTheme(ch);
}

function applyTheme(ch) {
    var element = document.body;
    element.className = "";
    if (ch === "light") {
        element.classList.add("light");
    } else if (ch === "dark") {
        element.classList.add("dark");
    } else {
        console.log("How?");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || "system";
    applyTheme(savedTheme);

    document.getElementById("mode").value = savedTheme;
});
