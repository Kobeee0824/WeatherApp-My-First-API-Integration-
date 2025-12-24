from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Fetch your API key from the environment
API_KEY = os.getenv("API_KEY")  # This loads the API key from the .env file correctly

# Home route
@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    city = ""

    if request.method == 'POST':
        city = request.form['city'].strip()  # Strip spaces from city name
        weather_data = get_weather_data(city)

    return render_template('index.html', weather_data=weather_data, city=city)


# Function to get weather data from OpenWeatherMap API
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    # Debugging: print the response status and content
    print(f"API Response Status Code: {response.status_code}")
    print(f"API Response Text: {response.text}")

    if response.status_code == 200:
        return response.json()  # Return the data in JSON format
    elif response.status_code == 404:
        return {"error": "City not found"}
    else:
        return {"error": f"An error occurred: {response.status_code}"}


if __name__ == '__main__':
    app.run(debug=True)
