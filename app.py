import requests
import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, url_for
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from sqlalchemy import or_
from forms import LoginForm, SignupForm
from models import db, connect_db, User, Diagnosis, UserHistory, Weather, Mood, Symptoms, CopingSolution
from datetime import datetime  # Import the datetime module
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

CURR_USER_KEY = "curr_user"

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
db.create_all()

##############################################################################
# User signup/login/logout
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global.""" 
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.user_id

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                registration_date=datetime.utcnow(),
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)  # Log in the user using do_login
        flash('Welcome! You have successfully signed up.', 'success')
        return redirect('/')
    
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Authenticate user
        user = User.authenticate(username, password)
        if user:
            do_login(user)  # Use the do_login function
            flash(f'Hello, {user.username}!', 'success')
            return redirect('/')
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Logout user."""
    try:
        session.pop(CURR_USER_KEY)
        flash("You have been logged out", "success")
    except KeyError:
        flash("You are not logged in", "danger")

    return redirect("/")



#_____________GETTING INFO FROM API_____________________________________
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




#________HOMEPAGE & USER PROFILES___________________
@app.route('/')
def homepage():
    if g.user:
        # Retrieve user history
        user_history = UserHistory.query.filter_by(user_id=g.user.user_id).all()

        # Retrieve information about friends (assuming you have a friends relationship)
        friends = g.user.friends  # Modify this according to your model structure

        # You can retrieve weather-related information here if needed
        # For example, you can make API calls to get weather data
        
        return render_template(
            'home.html',
            user_history=user_history,
            # friends=friends,
            user=g.user
        )
    else:
        return render_template('home-anon.html')