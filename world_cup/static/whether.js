window.addEventListener("DOMContentLoaded", async () => {
    loadWeather();
});

function loadWeather(){
    const apiKey = "9baff2747f9d922cf9139cb937c30940";
    let lat = document.getElementById("lat").value;
    let long = document.getElementById("long").value;
    const weatherURL =  "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + long + "&units=metric&appid=" + apiKey;
    fetch(weatherURL)
        .then(validateJSON)
        .then(displayWeather)
        .catch((error) => {console.log("OH NO!");})
} 

function displayWeather(data){
    console.log(data);
    const { name } = data;
    const { icon, description } = data.weather[0];
    const{ temp, humidity } = data.main;
    const { speed } = data.wind;
    console.log(name, icon, description, temp,humidity, speed);
    document.getElementById("city").innerText = "Weather Forecast";
    document.getElementById("icon").innerHTML = "https://openweathermap.org/img/wn/" + icon + "@2x.png";
    document.getElementById("description").innerText = description;
    document.getElementById("temp").innerText="Temperature: " + temp + "°C";
    document.getElementById("humidity").innerText = "Humidity: " + humidity + "%";
    document.getElementById("wind").innerText = "wind speed: " + speed + "km";
}

function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}
