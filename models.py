from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)

    user_history = db.relationship('UserHistory', back_populates='user', lazy='dynamic')

class Diagnosis(db.Model): #table stores information about main issues or diagnoses and is related to Coping Solutions.
    __tablename__ = 'diagnosis'

    issue_id = db.Column(db.Integer, primary_key=True)
    issue_name = db.Column(db.String(255), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'), nullable=False)

    solution_diagnosis = db.relationship('CopingSolution', back_populates='diagnosis')

class UserHistory(db.Model):
    __tablename__ = 'user_history'

    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather.weather_id'), nullable=False)
    mood_id = db.Column(db.Integer, db.ForeignKey('moods.mood_id'), nullable=False)
    symptom_id = db.Column(db.Integer, db.ForeignKey('symptoms.symptom_id'))
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.issue_id'))
    date_recorded = db.Column(db.Date, nullable=False)

    user = db.relationship('User', back_populates='user_history')
    weather = db.relationship('Weather', back_populates='user_history')
    mood = db.relationship('Mood', back_populates='user_history')
    symptom = db.relationship('Symptoms', foreign_keys=[symptom_id])
    diagnosis = db.relationship('Diagnosis', foreign_keys=[diagnosis_id])


class Weather(db.Model):
    __tablename__ = 'weather'

    weather_id = db.Column(db.Integer, primary_key=True)
    weather_date = db.Column(db.Date, nullable=False)
    temperature_value = db.Column(db.Float, nullable=False)
    temperature_unit = db.Column(db.String(10), nullable=False)

    # New fields for real-time weather data
    real_time_weather_type = db.Column(db.String(50), nullable=True)
    real_time_condition = db.Column(db.String(255), nullable=True)
    real_time_icon = db.Column(db.String(255), nullable=True)
    real_time_feelslike_f = db.Column(db.Float, nullable=True)
    real_time_feelslike_c = db.Column(db.Float, nullable=True)
    real_time_humidity = db.Column(db.Integer, nullable=True)
    real_time_uv_index = db.Column(db.Float, nullable=True)

    # New fields for forecast weather data
    forecast_weather_type = db.Column(db.String(50), nullable=True)
    forecast_condition = db.Column(db.String(255), nullable=True)
    forecast_icon = db.Column(db.String(255), nullable=True)
    forecast_high_temp_f = db.Column(db.Float, nullable=True)
    forecast_low_temp_f = db.Column(db.Float, nullable=True)
    forecast_high_temp_c = db.Column(db.Float, nullable=True)
    forecast_low_temp_c = db.Column(db.Float, nullable=True)

    # Relationship with UserHistory (one-to-one)
    user_history = db.relationship('UserHistory', uselist=False, back_populates='weather')

    # Other fields and relationships...


class Mood(db.Model): #table stores mood-related data and is related to Coping Solutions.
    __tablename__ = 'moods'

    mood_id = db.Column(db.Integer, primary_key=True)
    mood_date = db.Column(db.Date, nullable=False)
    mood_level = db.Column(db.Integer, nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'), nullable=False)

    solution = db.relationship('CopingSolution', back_populates='moods')

class Symptoms(db.Model): # table contains information about other symptoms and is related to Coping Solutions.
    __tablename__ = 'symptoms'

    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(255), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'), nullable=False)

    solution_symptoms = db.relationship('CopingSolution', back_populates='symptoms')

class CopingSolution(db.Model): #table contains solutions for Mood, Symptoms, Diagnosis.
    __tablename__ = 'coping_solutions'

    solution_id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False)

    diagnosis = db.relationship('Diagnosis', back_populates='solution_diagnosis')
    moods = db.relationship('Mood', back_populates='solution')
    symptoms = db.relationship('Symptoms', back_populates='solution_symptoms')

def connect_db(app):
    """Connect this database to the provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
    app.app_context().push()
    db.create_all()
