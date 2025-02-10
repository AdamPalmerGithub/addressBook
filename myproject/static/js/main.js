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

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(getAPI);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}
// needs to be global
window.getLocation = getLocation;

async function getAPI(position){
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}&current=temperature_2m,relative_humidity_2m&wind_speed_unit=mph&forecast_days=1`);
    const done = await res.json();
    let date = done.current.time.split("T")[0];
    let time = done.current.time.split("T")[1];
    date = date.split("-");
    const formatted_date = date[2] + "-" + date[1] + "-" + date[0];
    document.getElementById("time").innerHTML = "<strong>Time: </strong>" + time;
    document.getElementById("date").innerHTML = "<strong>Date: </strong>" + formatted_date;
    document.getElementById("temp").innerHTML = "<strong>Temperature: </strong>" + done.current.temperature_2m + "°C";
    document.getElementById("humidity").innerHTML = "<strong>Humidity: </strong>" + done.current.relative_humidity_2m + "%";
}
