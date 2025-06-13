import requests
import os
import uuid
import logging
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, url_for, send_from_directory
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import LoginForm, SignupForm, MoodSymptomAssessmentForm, ProfileEditForm, JournalEntryForm, DailyAssessmentForm
from models import db, connect_db, User, Diagnosis, UserHistory, Weather, CopingSolution, Group, JournalEntry, DailyAssessment, GroupPost, DiagnosisSolution, UserDiagnosisAssociation
from datetime import datetime, timedelta, date 
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from statistics import mean, mode
from werkzeug.utils import secure_filename
from sqlalchemy import update
from datetime import datetime, timedelta
from meteostat import Point, Daily
from geopy.geocoders import Nominatim
from utils.mood_weather_analysis import generate_weather_mood_insights
from utils.mood_predictor import predict_mood_score, interpret_mood_score

# from flask_wtf.csrf import CSRFProtect
from urllib.parse import quote
import traceback
import pandas as pd


CURR_USER_KEY = "curr_user"
# # # Initialize Flask-Migrate- USED WITH ANY UPDATE TO THE MODELS FOR DB MOODY
# migrate = Migrate(app, db)


app = Flask(__name__)

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%B %d'):
    """Convert string datetime to formatted date."""
    dt = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return dt.strftime(format)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///moody'))
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev-key")
# toolbar = DebugToolbarExtension(app)
# app.debug = True

# csrf = CSRFProtect(app)

connect_db(app)

if os.environ.get("FLASK_ENV") == "development":
    with app.app_context():
        db.create_all()
  


@app.route('/insights')
def mood_weather_insights():
    plot_paths = generate_weather_mood_insights()
    return render_template("api/insights.html", plot_paths=plot_paths)



##############################################################################
#_________________User signup/login/logout_______________________
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

@app.route('/demo_login')
def demo_login():
    demo_user = User.query.filter_by(username="demo").first()
    if demo_user:
        do_login(demo_user)
        flash("You are now using the demo account!", "info")
        return redirect('/')
    else:
        flash("Demo user not set up. Please contact support.", "danger")
        return redirect(url_for('login'))

##############################################################################
#_____________GETTING INFO FROM API_________________________
@app.route('/current', methods=['GET', 'POST'])
def current():
    current_weather_data = None
    predicted_mood_score = None
    mood_interpretation = None

    if request.method == 'POST':
        location = request.form.get('location')
        current_weather_data = get_current_weather(location)

        if current_weather_data:
            try:
                temp_f = current_weather_data['current']['temp_f']
                pressure = current_weather_data['current']['pressure_mb']
                predicted_mood_score = predict_mood_score(temp_f, pressure)
                mood_interpretation = interpret_mood_score(predicted_mood_score, temperature_f=temp_f, air_pressure_hpa=pressure)

            except Exception as e:
                print("Prediction error:", e)

    return render_template(
        'api/current.html',
        current_weather_data=current_weather_data,
        predicted_mood_score=predicted_mood_score,
        mood_interpretation=mood_interpretation,
        user=g.user
    )


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
    




API_KEY = os.getenv("OPENWEATHER_API_KEY") or "8abaef3552576b437483fe132d8fa8d9"

@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    forecast_data = None
    forecast_predictions = []
    forecast_items = []
    default_city = "New York" if g.user and g.user.username == "demo" else ""

    if request.method == "POST":
        location = request.form.get("location")

        try:
            geolocator = Nominatim(user_agent="moody_app")
            geo = geolocator.geocode(location)

            if not geo:
                flash("Could not find the specified location.")
                return render_template("api/forecast.html", forecast_data=None, zipped_forecast=[], default_city=default_city)

            lat, lon = geo.latitude, geo.longitude

            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
            res = requests.get(url)
            data = res.json()

            if data.get("cod") != "200":
                flash(f"Error: {data.get('message', 'Unable to fetch forecast')}")
                return render_template("api/forecast.html", forecast_data=None, zipped_forecast=[], default_city=default_city)

            forecast_data = data

            for item in data.get("list", []):
                if "12:00:00" in item["dt_txt"]:
                    temp = item["main"]["temp"]
                    pressure = item["main"]["pressure"]
                    score = predict_mood_score(temp, pressure)
                    interpretation = interpret_mood_score(score, temperature_f=temp, air_pressure_hpa=pressure)


                    forecast_items.append(item)
                    forecast_predictions.append({
                        "score": score,
                        "interpretation": interpretation
                    })

        except Exception as e:
            flash(f"Error fetching forecast: {str(e)}")

    zipped_forecast = zip(forecast_items, forecast_predictions)

    return render_template(
        "api/forecast.html",
        forecast_data=forecast_data,
        zipped_forecast=zipped_forecast,
        default_city=default_city
    )



@app.route('/history', methods=['GET', 'POST'])
def history():
    historical_weather_data = None  # Initialize outside POST check

    if request.method == 'POST':
        location = request.form.get('location')
        date = request.form.get('date')

        if location and date:
            historical_weather_data = get_historical_weather(location, date)
            if historical_weather_data:
                flash("Historical weather data successfully retrieved.", 'success')
            else:
                flash("Failed to fetch historical weather data. Please try again later.", 'error')
        else:
            flash("Please enter both location and date.", 'error')

    return render_template('api/history.html', historical_weather_data=historical_weather_data, user=g.user)



def get_historical_weather(location, date):
    try:
        # Convert date string to datetime object
        target_date = datetime.strptime(date, '%Y-%m-%d')

        # Geocode location
        geolocator = Nominatim(user_agent="moody_app")
        geo = geolocator.geocode(location)

        if not geo:
            flash("Location not found. Please enter a valid city.", 'error')
            return None

        lat, lon = geo.latitude, geo.longitude

        # Create Meteostat Point
        location_point = Point(lat, lon)

        # Fetch historical data for just one day
        data = Daily(location_point, target_date, target_date).fetch()

        if data.empty:
            flash("No data found for the given date/location.", 'error')
            return None

        row = data.iloc[0]
        historical = {
            "location": location.title(),
            "date": date,
            "temperature_f": round(row["tavg"] * 9 / 5 + 32, 1) if not pd.isna(row["tavg"]) else "N/A",
            "temperature_c": round(row["tavg"], 1) if not pd.isna(row["tavg"]) else "N/A",
            "humidity": row["rhum"] if "rhum" in row and not pd.isna(row["rhum"]) else "N/A",
            "precipitation_mm": row["prcp"] if not pd.isna(row["prcp"]) else "N/A",
            "wind_speed_kph": row["wspd"] * 3.6 if not pd.isna(row["wspd"]) else "N/A",
        }

        return historical

    except Exception as e:
        print("Error occurred in get_historical_weather:")
        traceback.print_exc()
        flash("An error occurred while retrieving historical data.", 'error')
        return None


@app.route('/astronomy', methods=['GET', 'POST'])
def astronomy():
    astronomy_data = None
    date = None  # Initialize date to None

    if request.method == 'POST':
        location = request.form.get('location')
        date = request.form.get('date')  # Get the date from the form
        astronomy_data = get_astronomy_data(location, date)

    return render_template('api/astronomy.html', astronomy_data=astronomy_data, date=date, user=g.user)


def get_astronomy_data(location, date):
    url = "https://weatherapi-com.p.rapidapi.com/astronomy.json"
    querystring = {"q": location, "dt": date}  # Include the date parameter if provided

    headers = {
        "X-RapidAPI-Key": "eb3fa9d2eamsh622acd4eaa00bf3p19fc73jsn647406a37c4e",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to fetch astronomy data for {location}. Please try again later.", 'error')
            return None
    except Exception as e:
        print("Error:", str(e))  # Add this line for debugging
        flash(f"An error occurred while fetching astronomy data for {location}. Please try again later.", 'error')
        return None
    

#____________On home page- Live weather updates!_________________________
@app.route('/set_location', methods=['POST'])
def set_location():
    location = request.form.get('location')

    if location:
        try:
            current_weather_data = get_current_weather(location)
            forecast_data = get_weather_forecast(location)

            if current_weather_data and forecast_data:
                if g.user:
                    g.user.location = location
                    db.session.commit()
                    flash('Location and weather data updated successfully!', 'success')
                else:
                    flash('User not found. Please log in.', 'error')
            else:
                flash('Failed to retrieve weather data for the given location.', 'error')

        except ValueError as ve:
            flash(str(ve), 'error')
        except Exception as e:
            flash(f'Unexpected error: {e}', 'error')
    else:
        flash('Please provide a location to update.', 'error')

    return redirect(url_for('homepage'))


def get_weather_forecast(location):
    API_KEY = os.getenv("OPENWEATHER_API_KEY") or "8abaef3552576b437483fe132d8fa8d9"

    # Restrict location only for demo user
    if g.user and g.user.username == "demo" and location.lower() != "new york":
        raise ValueError("Only New York supported for demo")

    try:
        # Get latitude and longitude using geopy
        geolocator = Nominatim(user_agent="moody_app")
        loc = geolocator.geocode(location)
        if not loc:
            raise ValueError("Location not found. Please enter a valid city name.")

        lat, lon = loc.latitude, loc.longitude

        # Call OpenWeatherMap 5-day forecast API
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial"
        res = requests.get(url)
        data = res.json()

        if data.get("cod") != "200":
            raise ValueError(data.get("message", "Unable to fetch forecast"))

        return data

    except Exception as e:
        print(f"Forecast error: {e}")
        return None


#######################################################################
#________HOMEPAGE & USER PROFILES___________________

@app.route("/")
def homepage():
    forecast_data = None
    current_weather_data = None
    mood_prediction = None
    predicted_mood_score = None
    image_url = None
    user_history = []
    user_groups = []
    latest_assessment = None
    today_date = date.today()
    location = None

    if g.user:
        user = g.user
        user_profile = User.query.filter_by(user_id=user.user_id).first()
        user_history = UserHistory.query.filter_by(user_id=user.user_id).all()
        user_groups = user.groups
        form = ProfileEditForm(request.form)
        image_url = user_profile.image_url if user_profile else None
        location = user.location

        # Default location if demo user with no location
        if user.username == "demo" and not location:
            location = "New York"

        if location:
            current_weather_data = get_current_weather(location)
            forecast_data = get_weather_forecast(location)

            if current_weather_data:
                weather_text = current_weather_data['current']['condition']['text']
                temperature = current_weather_data['current']['temp_f']
                pressure = current_weather_data['current']['pressure_mb']

                # (Optional) Basic text-based rule prediction
                # mood_prediction = predict_mood_from_weather(weather_text, temperature)

                # ML-based prediction
                predicted_mood_score = predict_mood_score(temperature, pressure)
                mood_interpretation = interpret_mood_score(predicted_mood_score, temperature_f=temperature, air_pressure_hpa=pressure)


        latest_assessment = DailyAssessment.query.filter_by(user_id=user.user_id).order_by(DailyAssessment.date.desc()).first()

        return render_template(
            'home.html',
            today_date=today_date,
            user=user,
            form=form,
            location=location,
            current_weather_data=current_weather_data,
            forecast_data=forecast_data,
            mood_prediction=mood_prediction,
            image_url=image_url,
            latest_assessment=latest_assessment,
            user_history=user_history,
            user_groups=user_groups,
            predicted_mood_score=predicted_mood_score,
            mood_interpretation=mood_interpretation,
        )

    # Not logged in
    return render_template("home-anon.html")



    

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if g.user is None:
        flash('You must be logged in to edit your profile.', 'warning')
        return redirect(url_for('login'))

    user = g.user
    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        # ✅ Correctly access the uploaded file
        uploaded_image = request.files.get("image_url")
        if uploaded_image and uploaded_image.filename != "":
            filename = secure_filename(uploaded_image.filename)
            unique_filename = str(uuid.uuid4()) + "_" + filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            uploaded_image.save(file_path)

            user.image_url = unique_filename

        # Update other fields
        user.bio = form.bio.data
        user.location = form.location.data

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('homepage'))

    return render_template('edit_profile.html', form=form, user=user)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)





#_______Friends_________
@app.route('/friends_profile/<int:user_id>')
def friends_profile(user_id):
    # Find the user by user_id
    user = User.query.get(user_id)
    user_profile = User.query.filter_by(user_id=user.user_id).first()
    image_url = user_profile.image_url if user_profile else None
    if user:
        # Retrieve the user's location (if available)
        location = user.location

        # Retrieve weather information for the user's location (if needed)???

        # Retrieve the groups the user is in
        user_groups = user.groups
        # Retrieve the user's friends
        friends = user.friends

        current_weather_data = None

        # If the user has a location, fetch the current weather data
        if location:
            current_weather_data = get_current_weather(location)
            
        return render_template('friends_profile.html', user=user, location=location, user_groups=user_groups, friends=friends, current_weather_data=current_weather_data, image_url=image_url)
    else:
        # Handle the case where the user is not found
        return "User not found"


@app.route('/send_friend_request/<int:user_id>', methods=['POST'])
def send_friend_request(user_id):
    if not g.user:
        # flash('Not logged in', 'error')
        return jsonify({'success': False, 'message': 'Not logged in'})

    if user_id == g.user.user_id:
        flash('Cannot send a friend request to yourself', 'error')
        return jsonify({'success': False, 'message': 'Cannot send a friend request to yourself'})

    recipient = User.query.get(user_id)

    if recipient:
        # Check if the recipient is already a friend
        if recipient in g.user.friends:
            # flash('You are already friends with this user', 'error')
            return jsonify({'success': False, 'message': 'You are already friends with this user'})

        # Check if the friend request already exists
        if g.user in recipient.friend_requests:
            # flash('Friend request already sent', 'error')
            return jsonify({'success': False, 'message': 'Friend request already sent'})

        # Add the sender to the recipient's friend requests
        recipient.friend_requests.append(g.user)
        db.session.commit()
        # flash('Friend request sent successfully', 'success')
        return jsonify({'success': True, 'message': 'Friend request sent successfully'})
    else:
        # flash('User not found', 'error')
        return jsonify({'success': False, 'message': 'User not found'})


@app.route('/accept_friend_request/<int:sender_id>', methods=['POST'])
def accept_friend_request(sender_id):
    if not g.user:
        return jsonify(success=False, message='Not logged in')

    sender = User.query.get(sender_id)

    if sender:
        # Check if the sender has sent a friend request to the current user
        if sender in g.user.friend_requests:
            # Remove the friend request
            g.user.friend_requests.remove(sender)
            # Add the sender to the current user's list of friends
            g.user.friends.append(sender)

            # Add the current user to the sender's list of friends
            sender.friends.append(g.user)

            db.session.commit()
            return jsonify(success=True, message='Friend request accepted')
        else:
            return jsonify(success=False, message='Friend request not found')
    else:
        return jsonify(success=False, message='User not found')


# remove a friend
@app.route('/remove_friend/<int:friend_id>', methods=['POST'])
def remove_friend(friend_id):
    if not g.user:
        # Check if the user is logged in
        flash('Not logged in', 'error')
        return redirect(url_for('friends_groups')) 

    friend = User.query.get(friend_id)
    if friend:
        # Check if the friend exists
        if friend in g.user.friends:
            # Remove the friend from the user's friends list
            g.user.friends.remove(friend)
            db.session.commit()
            flash('Friend removed successfully', 'success')
        else:
            flash('User is not your friend', 'error')
    else:
        flash('Friend not found', 'error')

    return redirect(url_for('friends_groups'))  


###############################################################################
#_______________________Assessments__________________________________
# Updated function to determine the diagnosis
def determine_diagnosis(form_data):
    diagnoses = set()
#2
    if form_data.get('experienced_sad_disaster') == 'yes': 
        diagnoses.add(2)

    if form_data.get('estorms') == 'yes':
        diagnoses.add(2)

    print(f'experienced_sad_disaster: {form_data.get("experienced_sad_disaster")}')
    print(f'estorms: {form_data.get("estorms")}')

#3
    mood_symptoms = [
        'mood_swings_weather',
        'mood_variation_weather',
        'weather_mood_beliefs',
    ]
    if any(form_data.get(symptom) == 'yes' for symptom in mood_symptoms):
        diagnoses.add(3)

#4
    sad_symptoms = [
        'experienced_sad',
        'seasonal_affective_disorder',
        'experienced_geographic_changes',
        'geographic_location',
        'impact_relocation',
    ]
    if any(form_data.get(symptom) == 'yes' for symptom in sad_symptoms):
        diagnoses.add(4)

#5
    lifestyle_factors = [
        'positive_affect_threshold',
        'diet_influence',
        'emotional_support',
    ]
    if any(form_data.get(factor) == 'yes' for factor in lifestyle_factors):
        diagnoses.add(5)

#6
    if form_data.get('outdoor_activities') == 'yes':
        diagnoses.add(6)

    # Define the list of physical symptoms choices
    physical_symptoms_choices = [
        'headache',
        'joint_pain',
        'migraine',
        'sinus_congestion',
        'fatigue',
        'nausea',
        'allergies',
        'sore_throat',
        'stiffness',
        'shortness_of_breath',
        'other',
    ]
  # Get the values of physical symptoms from the form data
    physical_symptoms_values = form_data.getlist('physical_symptoms')
    # Check if any of the physical symptoms checkboxes are checked
    if any(symptom in physical_symptoms_values for symptom in physical_symptoms_choices):
        diagnoses.add(6)

    #1
    if form_data.get('climate_anxiety') == 'yes' or form_data.get('social_interaction') == 'yes':
        diagnoses.add(1)

    return list(diagnoses)


@app.route('/mood_symptom', methods=['GET', 'POST'])
def mood_symptom():
    form = MoodSymptomAssessmentForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Get the form data
        form_data = request.form

        # Determine the diagnoses
        diagnosis_ids = determine_diagnosis(form_data)

        # Create a dictionary to store the diagnoses
        diagnosis_data = {}

        for diagnosis_id in diagnosis_ids:
            diagnosis = Diagnosis.query.get(diagnosis_id)
            if diagnosis:
                diagnosis_name = diagnosis.issue_name
                solution_texts = [solution.solution_text for solution in diagnosis.solutions]
                diagnosis_data[diagnosis_name] = solution_texts

                # Check if the user already has this diagnosis in their history
                existing_diagnosis = UserDiagnosisAssociation.query.filter_by(
                    user_id=g.user.user_id,
                    diagnosis_id=diagnosis_id
                ).first()

                if not existing_diagnosis:
                    user_diagnosis_association = UserDiagnosisAssociation(
                        user_id=g.user.user_id,
                        diagnosis_id=diagnosis_id,
                        date_recorded=date.today()
                    )
                    db.session.add(user_diagnosis_association)

        # Commit the new UserDiagnosisAssociation entries to the database
        db.session.commit()

        # Render a response, providing the diagnoses and solutions to the user
        return render_template('diagnosis.html', diagnosis_data=diagnosis_data)

    return render_template('mood_symptom_form.html', form=form)


# Create a function to map issue_id to group_name
def map_issue_to_group(issue_id):
    issue_group_mapping = {
        1: "Climate Change Anxiety",
        2: "Major Disaster/Severe Weather Anxiety",
        3: "Weather makes me moody",
        4: "SAD",
        5: "General Weather Stress/ Cabin Fever",
        6: "Weather & Physical Health",
    }
    return issue_group_mapping.get(issue_id, "N/A")


@app.route('/diagnosis_history', methods=['GET'])
def diagnosis_history():
    if not g.user:
        return jsonify(success=False, message='Not logged in')

    # Retrieve the user's history based on the user_id attribute
    user_id = g.user.user_id

    # Query the database to retrieve the user's history based on user_id
    user_history = UserDiagnosisAssociation.query.filter_by(user_id=user_id).all()

    # Create a dictionary to store the user's diagnosis history
    diagnosis_data = {}

    for entry in user_history:
        diagnosis = Diagnosis.query.get(entry.diagnosis_id)
        if diagnosis:
            diagnosis_name = diagnosis.issue_name
            recommended_group_name = map_issue_to_group(diagnosis.issue_id)
            diagnosis_data[diagnosis_name] = {
                "recommended_group_name": recommended_group_name,
            }

    for entry in user_history:
        diagnosis = Diagnosis.query.get(entry.diagnosis_id)
        if diagnosis:
            diagnosis_name = diagnosis.issue_name
            solution_texts = [solution.solution_text for solution in diagnosis.solutions]
            diagnosis_data[diagnosis_name] = solution_texts

    return render_template('diagnosis_history.html', user_history=user_history, diagnosis_data=diagnosis_data, map_issue_to_group=map_issue_to_group)


@app.route('/daily_assessment', methods=['GET', 'POST'])
def daily_assessment():
    form = DailyAssessmentForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Convert selected values to integers
        stress_level = int(form.stress_level.data[0]) if form.stress_level.data else 0  # Set a default value (e.g., 0) if the list is empty
        positive_affect_rating = int(form.positive_affect_rating.data[0]) if form.positive_affect_rating.data else 0
 

        #  the assessment object and insert it into the database
        assessment = DailyAssessment(
            user_id=g.user.user_id,
            date=datetime.now().date(),
            weather_today=','.join(form.weather_today.data),
            mood_today=','.join(form.mood_today.data),
            stress_level=stress_level,
            positive_affect_rating=positive_affect_rating
        )

        db.session.add(assessment)
        db.session.commit()

        return redirect(url_for('homepage'))

    return render_template('daily_assessment.html', form=form)


###############################################################################
#_______________________Friends & Groups______________________________________
@app.route('/friends_groups', methods=['GET', 'POST'])
def friends_groups():
    # List all available groups
    groups = Group.query.all()

    # Initialize the users variable to None
    users = None

    # Fetch the user's friend requests received
    friend_requests_received = g.user.friend_requests  # Assuming you have a 'friend_requests' relationship

    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Use a case-insensitive filter to search for users by username
            users = User.query.filter(User.username.ilike(f'%{query}%')).all()

    # If no users are found, return all users
    if users is None:
        users = User.query.all()

    # Fetch the user's groups
    user_groups = g.user.groups

    # Create a dictionary to store whether the user is a member of each group
    group_membership = {group.group_id: g.user in group.members for group in groups}

    return render_template(
        'friends_groups/friends_groups.html',
        groups=groups,
        users=users,
        user=g.user,
        group_membership=group_membership,
        friend_requests_received=friend_requests_received  # Pass friend requests to the template
    )


@app.route('/join_group/<int:group_id>', methods=['GET', 'POST'])
def join_group(group_id):
    if not g.user:
        # Handle the case when the user is not logged in
        flash('You must be logged in to join a group.', 'warning')
        return jsonify(success=False, message='Not logged in')

    group = Group.query.get(group_id)

    if group:
        # Check if the user is already a member
        is_member = g.user in group.members

        if is_member:
            flash(f'Member: Let\'s chat with the group "{group.group_name}".', 'success')
        else:
            # Add the user to the group's members and save the relationship
            g.user.groups.append(group)
            db.session.commit()
            flash(f'Welcome to the group "{group.group_name}".', 'success')
            print(f'Joined group {group.group_name} with ID {group_id}')

        # Determine the message to send to the frontend
        message = 'Joined the group' if not is_member else 'Already a member'

        return jsonify(success=True, message=message, group_id=group_id, user=g.user)
    
    flash('Group not found', 'danger')
    return jsonify(success=False, message='Group not found')


@app.route('/leave_group/<int:group_id>', methods=['POST'])
def leave_group(group_id):
    if g.user:
        group = Group.query.get(group_id)
        if group:
            if g.user in group.members:
                group.members.remove(g.user)
                db.session.commit()
                return jsonify(success=True, message='Left the group', group_id=group_id)
    return jsonify(success=False, message='Failed to leave the group')



@app.route('/group/<int:group_id>', methods=['GET', 'POST'])
def group(group_id):
    group = Group.query.get(group_id)

    if request.method == 'POST':
        post_content = request.form.get('post_content')

        if post_content:
            current_user_id = g.user.user_id
            new_post = GroupPost(user_id=current_user_id, group=group, post_content=post_content)
            db.session.add(new_post)
            db.session.commit()

            
            return jsonify({
                'username': new_post.user.username,
                'content': new_post.post_content,
                'timestamp': new_post.timestamp,
                'post_id': new_post.id,
                'user_id': new_post.user_id
            })

    posts = GroupPost.query.filter_by(group=group).all()

    for post in posts:
    # Format the timestamp as a string
        post.timestamp_str = post.timestamp.strftime('%Y-%m-%d %H:%M:%S')

    return render_template('friends_groups/group.html', group=group, posts=posts, user=g.user)
# csrf_token=csrf.generate_csrf()


@app.route('/get_group_members/<int:group_id>', methods=['GET'])
def get_group_members(group_id):
    # Query the database to retrieve group members for the given group_id
    group = Group.query.get(group_id)

    if group is not None:
        members = group.members
        member_data = [{'username': member.username} for member in members]
        return jsonify(member_data)

    return jsonify([])  # Return an empty list if the group is not found



#______________GROUP POSTS_________________________
# Group creation, response creation, and post deletion routes
@app.route('/create_group_post/<int:group_id>', methods=['POST'])
def create_group_post(group_id):
    if g.user:
        post_content = request.form.get('post_content')
        if post_content:
            new_post = GroupPost(post_content=post_content, group_id=group_id, user_id=g.user.user_id)
            db.session.add(new_post)
            db.session.commit()

            # Return JSON response
            return jsonify({
                'username': g.user.username,
                'content': new_post.post_content,
                'timestamp': new_post.timestamp,
                'post_id': new_post.id,
                'user_id': new_post.user_id
            })

    return jsonify({'error': 'Failed to create a new post'}), 500


@app.route('/create_response/<int:group_id>/<int:post_id>', methods=['POST'])
def create_response(group_id, post_id):
    if g.user:
        response_content = request.form.get('response_content')
        if response_content:
            new_response = GroupPost(response_content=response_content, group_id=group_id, user_id=g.user.user_id, parent_post_id=post_id)
            db.session.add(new_response)
            db.session.commit()
    return redirect(url_for('group', group_id=group_id))


@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = GroupPost.query.get(post_id)
    if post and g.user and post.user_id == g.user.user_id:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('group', group_id=post.group_id))


##############################################################################
#________________WELLNESS- JOURNAL__________________________________
# Function to calculate the top N values from a list
def top_n_values(lst, n):
    return sorted(lst, reverse=True)[:n]

@app.route('/wellness', methods=['GET', 'POST'])
def wellness():
    form = JournalEntryForm()
    today_date = date.today()

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        user_id = g.user.user_id
    else:
        g.user = None
        user_id = None

    top_moods = []  # Initialize top_moods as an empty list

    if form.validate_on_submit() and user_id:
        existing_entry = JournalEntry.query.filter_by(
            user_id=user_id,
            date=form.date.data,
        ).first()

        if existing_entry:
            existing_entry.entry = form.entry.data
        else:
            new_entry = JournalEntry(
                user_id=user_id,
                date=form.date.data,
                entry=form.entry.data,
            )
            db.session.add(new_entry)

        db.session.commit()

    user_journal_entries = []
    if user_id:
        user_journal_entries = JournalEntry.query.filter_by(user_id=user_id).all()

#________________
    latest_assessment = DailyAssessment.query.filter_by(user_id=g.user.user_id).order_by(DailyAssessment.date.desc()).first()


    user_location = g.user.location

    mood_history_entries = DailyAssessment.query.filter_by(user_id=g.user.user_id).all()

# Initialize lists for the entries
    mood_entries = []
    stress_entries = []
    positive_affect_entries = []
    weather_entries = []

    for entry in mood_history_entries:
        # Mood entries
        mood_entries.append(entry.mood_today)  # Append each mood entry

        # Stress entries
        stress_level_text = str(entry.stress_level).strip("{}").split(" - ")[0]
        if stress_level_text.isdigit():
            stress_entries.append(int(stress_level_text))
        else:
            stress_entries.append(0)  # Set to 0 for invalid values

        # Positive affect entries
        rating_text = str(entry.positive_affect_rating).strip("{}").split(" - ")[0]
        if rating_text.isdigit():
            positive_affect_entries.append(int(rating_text))
        else:
            positive_affect_entries.append(0)  # Set to 0 for invalid values

        # Weather entries
        weather_entries.extend(entry.weather_today)

    # Calculate the top three moods
    if mood_entries:
        top_mood_values = top_n_values(mood_entries, 3)
        top_moods = list(set(top_mood_values))  # Remove duplicates
        top_moods = [str(mood) for mood in top_moods]
        average_mood = ', '.join(top_moods)
    else:
        average_mood = "No data"

    # Calculate the average stress level and positive affect rating
    if stress_entries:
        average_stress_level = mean(stress_entries)
    else:
        average_stress_level = "No data"

    if positive_affect_entries:
        average_positive_affect_rating = mean(positive_affect_entries)
    else:
        average_positive_affect_rating = "No data"

    # Calculate the most common weather
    if weather_entries:
        most_common_weather = mode(weather_entries)
    else:
        most_common_weather = "No data"

    # Get the weather choices for today from the form
    weather_today_choices = latest_assessment.weather_today if latest_assessment else []

    # Render the template
    return render_template(
        'wellness.html',
        today_date=today_date,
        form=form,
        user_journal_entries=user_journal_entries,
        user_location=user_location,
        latest_assessment=latest_assessment,
        most_common_weather=most_common_weather,
        average_mood=average_mood,
        average_stress_level=average_stress_level,
        average_positive_affect_rating=average_positive_affect_rating,
        top_moods=top_moods,
        mood_history_entries=mood_history_entries,
        weather_today_choices=weather_today_choices
    )


@app.route('/save_journal_entry', methods=['POST'])
def save_journal_entry():
    try:
        data = request.get_json()
        entry_text = data.get('entry')
        user_id = session.get(CURR_USER_KEY)

        print("Received data:", data)

        new_entry = JournalEntry(
            user_id=user_id,
            date=datetime.utcnow().date(),
            entry=entry_text
        )

        db.session.add(new_entry)

# Before the commit, print the entry to check if it's correctly populated
        print("New entry:", new_entry)

        db.session.commit()
        print("Journal entry saved successfully")

        return jsonify(success=True, message='Journal entry saved successfully')
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return jsonify(success=False, message='Failed to save journal entry')
    
@app.route('/fetch_journal_entries', methods=['GET'])
def fetch_journal_entries():
    # Get the user ID (assuming it's stored in session)
    user_id = session.get(CURR_USER_KEY)

    # Fetch journal entries for today's date and the current user (if logged in)
    today = datetime.today().strftime('%Y-%m-%d')
    entries = JournalEntry.query.filter_by(date=today, user_id=user_id).all()

    # Return the journal entries as JSON
    return jsonify([entry.serialize() for entry in entries])


@app.route('/edit_journal_entry/<int:id>', methods=['GET', 'POST'])
def edit_journal_entry(id):
    # Get the user's ID
    user_id = session.get(CURR_USER_KEY)

    # Fetch the journal entry for the specified ID and user
    journal_entry = JournalEntry.query.get(id)

    if not journal_entry or journal_entry.user_id != user_id:
        # Handle the case where the entry doesn't exist or doesn't belong to the user
        flash("Journal entry not found or unauthorized access.", "danger")
        return redirect(url_for('wellness'))  # Redirect to the wellness page or show an error message

    form = JournalEntryForm(obj=journal_entry)

    if form.validate_on_submit():
        # Update the journal entry with the submitted data
        form.populate_obj(journal_entry)  # Update the journal entry from the form data
        db.session.commit()
        flash("Journal entry updated successfully.", "success")
        return redirect(url_for('wellness'))  # Redirect back to the wellness page after editing

    return render_template('edit_journal.html', form=form, id=journal_entry.id, date=journal_entry.date, entry=journal_entry)

                           
@app.route('/delete_journal_entry/<int:id>', methods=['POST'])
def delete_journal_entry(id):
    if request.method == 'POST':
        entry_id = request.form.get('id')

        print(f"Deleting entry with id: {entry_id}")

        entry = JournalEntry.query.get(entry_id)
            
        if entry:
                # Check if the entry belongs to the logged-in user to prevent unauthorized deletion
            if entry.user_id == session.get(CURR_USER_KEY):
                    print("Entry found and user authorized for deletion.")
                    db.session.delete(entry)
                    db.session.commit()
                    print("Entry deleted.")
                    return redirect(url_for('wellness'))
            else:
                    print("User is not authorized for deletion.")
        else:
                print("Entry not found.")

    print("Invalid request or entry not deleted.")
    return redirect(url_for('wellness'))







