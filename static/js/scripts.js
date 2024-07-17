document.getElementById('city-input').addEventListener('input', function () {
    const query = this.value;
    if (query.length > 0) {
        fetch(`/autocomplete/${query}`)
            .then(response => response.json())
            .then(data => {
                const suggestions = document.getElementById('suggestions');
                suggestions.innerHTML = '';
                data.forEach(city => {
                    const li = document.createElement('li');
                    li.textContent = city;
                    li.onclick = () => {
                        document.getElementById('city-input').value = city;
                        suggestions.innerHTML = '';
                    };
                    suggestions.appendChild(li);
                });
            });
    }
});

// Функция для чтения куки
const getCookie = (name) => (
    document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
)

console.log(getCookie('last_city'))
if (getCookie('last_city') != null) {
    document.getElementById("city-input").value = getCookie('last_city');
}

function formatDateTime(dateTimeStr) {
    const date = new Date(dateTimeStr);

    const day = ('0' + date.getDate()).slice(-2);
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);

    const formattedDateTime = `${day}.${month} ${hours}:${minutes}`;

    return formattedDateTime;
}

function formatWeatherData(weatherData) {
    let formattedData = `<h2>Прогноз погоды для ${weatherData.city}</h2>`;
    formattedData += `<table><tr><th>Время</th><th>Температура (°C)</th></tr>`;
    weatherData.weather.forEach(entry => {
        formattedData += `<tr><td>${formatDateTime(entry.time)}</td><td>${entry.temperature}</td></tr>`;
    });
    formattedData += `</table>`;
    return formattedData;
}

function formatHistoryData(historyData) {
    let formattedData = `<h2>Статистика</h2>`;
    formattedData += `<table><tr><th>Город</th><th>Кол-во запросов</th></tr>`;
    historyData.forEach(entry => {
        formattedData += `<tr><td>${entry.city}</td><td>${entry.count}</td></tr>`;
    });
    formattedData += `</table>`;
    return formattedData;
}

function getWeather() {
    const city = document.getElementById('city-input').value;
    fetch(`/weather/${city}`)
        .then(response => {
            const setCookieHeader = response.headers.get('set-cookie');
            console.log('Set-Cookie Header:', setCookieHeader); // Для отладки
            return response.json();
        })
        .then(data => {
            if (data.error) {
                document.getElementById('weather-result').innerHTML = `<p>${data.error}</p>`;
            } else {
                document.getElementById('weather-result').innerHTML = formatWeatherData(data);
            }
        });
}

async function getHistory() {
    try {
        const response = await fetch('/history/');
        const data = await response.json();
        if (data.error) {
            document.getElementById('history-result').innerHTML = `<p>${data.error}</p>`;
        } else {
            document.getElementById('history-result').innerHTML = formatHistoryData(data);
        }
    } catch (error) {
        console.error('Error fetching history data:', error);
    }
}
