import requests
import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from sqlalchemy import or_
# from forms import UserAddForm, LoginForm, MessageForm, UserProfileForm
from models import db, connect_db
from datetime import datetime  # Import the datetime module


# CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///moody'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "JDOERR13"
toolbar = DebugToolbarExtension(app)

app.debug = True


connect_db(app)
app.app_context().push()
# db.drop_all()
# db.create_all()


@app.route('/current', methods=['GET', 'POST'])
def current():
    current_weather_data = None

    if request.method == 'POST':
        location = request.form.get('location')
        current_weather_data = get_current_weather(location)

    # If no location has been submitted, set current_weather_data to None
    if not current_weather_data:
        current_weather_data = None

    return render_template('current.html', current_weather_data=current_weather_data)

def get_current_weather(location):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    querystring = {"q": location}  # Use the user-provided location
    headers = {
        "X-RapidAPI-Key": "eb3fa9d2eamsh622acd4eaa00bf3p19fc73jsn647406a37c4e",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to fetch weather data for {location}. Please try again later.", 'error')
            return None
    except Exception as e:
        print("Error:", str(e))  # Add this line for debugging
        flash(f"An error occurred while fetching weather data for {location}. Please try again later.", 'error')
        return None
    
@app.route('/forecast', methods=['GET', 'POST'])
def forecast():
    forecast_data = None

    if request.method == 'POST':
        location = request.form.get('location')
        forecast_data = get_weather_forecast(location)

    return render_template('forecast.html', forecast_data=forecast_data)

def get_weather_forecast(location):
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": location, "days": "3"}  # Use the user-provided location and request a 3-day forecast
    headers = {
        "X-RapidAPI-Key": "eb3fa9d2eamsh622acd4eaa00bf3p19fc73jsn647406a37c4e",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to fetch weather forecast for {location}. Please try again later.", 'error')
            return None
    except Exception as e:
        print("Error:", str(e))  # Add this line for debugging
        flash(f"An error occurred while fetching weather forecast for {location}. Please try again later.", 'error')
        return None
    


@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        location = request.form.get('location')
        date = request.form.get('date')

        if location and date:
            historical_weather_data = get_historical_weather(location, date)
            if historical_weather_data:
                return render_template('history.html', historical_weather_data=historical_weather_data)
            else:
                flash("Failed to fetch historical weather data. Please try again later.", 'error')
        else:
            flash("Please enter both location and date.", 'error')

    return render_template('history.html', historical_weather_data=None)




def get_historical_weather(location, date):
    # Convert the date string to a datetime object (if needed)
    # Example format: 'YYYY-MM-DD'
    try:
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
    except ValueError:
        flash("Invalid date format. Please use YYYY-MM-DD format.", 'error')
        return None

    url = "https://weatherapi-com.p.rapidapi.com/history.json"
    querystring = {
        "q": location,
        "dt": formatted_date,  # Use the formatted date
        "lang": "en"
    }

    headers = {
        "X-RapidAPI-Key": "eb3fa9d2eamsh622acd4eaa00bf3p19fc73jsn647406a37c4e",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to fetch historical weather data for {location}. Please try again later.", 'error')
            return None
    except Exception as e:
        print("Error:", str(e))  # Add this line for debugging
        flash(f"An error occurred while fetching historical weather data for {location}. Please try again later.", 'error')
        return None




