from flask import Flask, render_template, request
import requests
from urllib.parse import quote_plus

def get_city_image_url(city):
    label = quote_plus(city.strip() or "City")
    return f"https://loremflickr.com/900/420/{label}"


def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    current = data["current_condition"][0]
    temp_c = current["temp_C"]
    weather_desc = current["weatherDesc"][0]["value"]
    humidity = current["humidity"]
    feels_like = current["FeelsLikeC"]
    wind_speed = current["windspeedKmph"]

    windy = int(wind_speed) > 10
    raining = "rain" in weather_desc.lower()
    image_url = get_city_image_url(city)

    return {
        "location": city,
        "temperature_c": temp_c,
        "feels_like_c": feels_like,
        "condition": weather_desc,
        "humidity": humidity,
        "windy": windy,
        "raining": raining,
        "image_url": image_url,
    }

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    lang = request.args.get('lang', 'en')
    if request.method == 'POST':
        city = request.form['city']
        weather = get_weather(city)
        return render_template('result.html', weather=weather, lang=lang)
    return render_template('index.html', lang=lang)

if __name__ == '__main__':
    app.run(debug=True)