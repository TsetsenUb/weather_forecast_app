function getWeatherIcon(iconCode) {
    const iconMap = {
        "01d": "☀️",
        "01n": "🌙",
        "02d": "⛅",
        "02n": "☁️",
        "03d": "☁️",
        "03n": "☁️",
        "04d": "☁️",
        "04n": "☁️",
        "09d": "🌧️",
        "09n": "🌧️",
        "10d": "🌦️",
        "10n": "🌦️",
        "11d": "⛈️",
        "11n": "⛈️",
        "13d": "❄️",
        "13n": "❄️",
        "50d": "🌫️",
        "50n": "🌫️"
    };
    return iconMap[iconCode] || "🌈";
}

function getCurrentWeather(data, currentForecast) {
    return `
    <div class="location-info">
        <div class="location-item">
            <span class="location-label">Город</span>
            <span class="location-name"><strong>${data.name}</strong></span>
        </div>
        <div class="location-item">
            <span class="location-label">Страна</span>
            <span class="location-value">${data.country}</span>
        </div>
        <div class="location-item">
            <span class="location-label">Координаты</span>
            <span class="location-value">${data.lat}°, ${data.lon}°</span>
        </div>
        <div class="location-item">
            <span class="location-label">Дата</span>
            <span class="location-value">
                ${currentForecast.dt_date}
                ${currentForecast.dt_time}
            </span>
        </div>
    </div>
    <div class="current-forecast">
        <div class="weather-icon">
            ${getWeatherIcon(currentForecast.weather_icon)}
        </div>
        <div class="temperature">
            ${currentForecast.temperature}°C
        </div>
        <div class="weather-details">
            <div class="weather-description">
                ${currentForecast.weather_description}
            </div>
            <div class="detail-item">
                💧 ${currentForecast.humidity}%
                📊 ${currentForecast.pressure} мм
            </div>
        </div>
        <div class="weather-details">
            <div class="detail-item">
                💨 ${currentForecast.wind_speed} м/с
            </div>
            <div class="detail-item">
                🧭 ${currentForecast.wind_direction}
            </div>
            <div class="detail-item">
                🕐 ${currentForecast.dt_time}
            </div>
        </div>
    </div>
    `;
}

function getDayForecasts(currentDayForecasts) {

    return currentDayForecasts
    .map(forecast => `
        <div class="forecast-card">
            <div class="forecast-time">
                ${forecast.dt_time}
            </div>
            <div class="forecast-content">
                <div class="forecast-icon">
                    ${getWeatherIcon(forecast.weather_icon)}
                </div>
                <div class="forecast-details">
                    <div class="forecast-temperature">
                        ${forecast.temperature}°C
                    </div>
                    <div class="forecast-description">
                        ${forecast.weather_description}
                    </div>
                    <div class="forecast-stat">
                        💧 ${forecast.humidity}%
                        📊 ${forecast.pressure} мм
                    </div>
                    <div class="forecast-stat">
                        💨 ${forecast.wind_speed} м/с
                        🧭 ${forecast.wind_direction}
                    </div>
                </div>
            </div>
        </div>
    `)
    .join("");
}

function getFollowingDayForecasts (daysForecasts, start_indx=1) {
    let res = `
    <summary class="f-days-summary" id="fDaysSummary">
        Посмотреть прогноз на пять суток
    </summary>
    `;

    for (let i = start_indx; i < daysForecasts.length; i++) {
        res += `
        <div class="following-days-date"><b>${daysForecasts[i][0].dt_date}</b></div>
        <div class="hourly-forecasts" id="hourlyForecasts">
            ${getDayForecasts(daysForecasts[i])}
        </div>
        `
    }

    res += "<div class='f-days-summary-bottom'><div>"

    return res;
}

function displayWeatherData(data) {
    const currentWeather = document.getElementById("currentWeather");
    const hourlyForecasts = document.getElementById("hourlyForecasts");
    const followingDays = document.getElementById("followingDays");

    errorMessage.classList.remove("active");

    if (!data.forecasts || data.forecasts.length === 0) {
        throw new Error("Нет данных о прогнозе погоды");
    }

    const daysForecasts = data.forecasts;
    const currentDayForecasts = daysForecasts[0];

    if (!currentDayForecasts || currentDayForecasts.length === 0) {
        throw new Error("Нет данных о текущей погоде");
    }

    currentWeather.innerHTML = getCurrentWeather(data, currentDayForecasts[0]);

    hourlyForecasts.innerHTML = getDayForecasts(currentDayForecasts.slice(1));

    followingDays.innerHTML = getFollowingDayForecasts(daysForecasts);

    weatherSection.classList.add("active");
}

async function getAndDisplayForecast () {
    const city = document.getElementById("cityInput").value.trim();
    if (!city) return;

    const loading = document.getElementById("loading");
    const weatherSection = document.getElementById("weatherSection");
    const errorMessage = document.getElementById("errorMessage");

    loading.style.display = "block";
    weatherSection.classList.remove("active");
    errorMessage.classList.remove("active");

    try {
        const res = await fetch(`http://localhost:8000/api/forecast/?city=${encodeURIComponent(city)}`);

        if (!res.ok) {
            throw new Error("Город не найден или произошла ошибка сервера");
        }

        const data = await res.json();
        displayWeatherData(data);

    } catch (error) {
        console.error("Ошибка:", error);
        errorMessage.textContent = error.message || "Произошла ошибка при получении данных";
        errorMessage.classList.add("active");
    } finally {
        loading.style.display = "none";
    }
}
