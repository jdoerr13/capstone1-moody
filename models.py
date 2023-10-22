from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref, registry


# Create a SQLAlchemy instance
db = SQLAlchemy()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Register the mapper
mapper_registry = registry()

# Define the user_group_association table for many-to-many relationship- SHOW THE GROUPS THE USER IS IN
user_group_association = db.Table(
    'user_group_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.group_id')),
    extend_existing=True,
)

# Association table for friends - Allows many-to-many relationships between users in the application. SHOWS FRIENDS
user_friends = db.Table(  
    'user_friends',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)

# Association table representing & MANAGING friend requests between users.
user_friend_requests = db.Table(
    'user_friend_requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('receiver_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)


class DiagnosisSolution(db.Model):
    __tablename__ = 'diagnosis_solutions'

    id = db.Column(db.Integer, primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.issue_id'))
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'))

    diagnosis = db.relationship('Diagnosis', back_populates='solutions')
    solution = db.relationship('CopingSolution', back_populates='diagnoses')

class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'

    issue_id = db.Column(db.Integer, primary_key=True)
    issue_name = db.Column(db.String(255), nullable=False)

    solutions = db.relationship('DiagnosisSolution', back_populates='diagnosis')

class CopingSolution(db.Model): #table contains solutions for Mood, Symptoms, Diagnosis.
    __tablename__ = 'coping_solutions'

    solution_id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False)

    diagnoses = db.relationship('DiagnosisSolution', back_populates='solution')
    moods = db.relationship('Mood', back_populates='solution')
    symptoms = db.relationship('Symptoms', back_populates='solution')






class JournalEntry(db.Model):
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    entry = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('journal_entries', lazy=True))

    def __init__(self, user_id, date, entry):
        self.user_id = user_id
        self.date = date
        self.entry = entry

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.strftime('%Y-%m-%d'),  # Format the date as a string
            'entry': self.entry,
        }   

# User model
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(255))  # Add the image_url column
    location = db.Column(db.String(255))
    bio = db.Column(db.Text)  # Add the bio column as a text field
    # Add a field for the user's profile picture URL
    image_url = db.Column(db.String(255))  # This field will store the profile picture URL


    user_history = db.relationship('UserHistory', back_populates='user', lazy='dynamic')

    # Relationship for friends
    friends = db.relationship(
        'User',
        secondary=user_friends,
        primaryjoin=(user_friends.c.user_id == user_id),
        secondaryjoin=(user_friends.c.friend_id == user_id),
        backref=db.backref('user_friends', lazy='dynamic'),
    )

    # Relationship for friend requests
    friend_requests = db.relationship(
        'User',
        secondary=user_friend_requests,
        primaryjoin=(user_friend_requests.c.sender_id == user_id),
        secondaryjoin=(user_friend_requests.c.receiver_id == user_id),
        backref=db.backref('user_friend_requests', lazy='dynamic'),
    )

    # Add the many-to-many relationship with groups
    groups = db.relationship(
        'Group',
        secondary=user_group_association,
        back_populates='members',  # Updated back_populates name
    )

    
    @classmethod
    def signup(cls, username, email, password, registration_date):
        """Sign up user.

        Hashes password and adds user to the system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            registration_date=registration_date,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return None

class DailyAssessment(db.Model):
    __tablename__ = 'daily_assessment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Use 'users' as the table name
    date = db.Column(db.Date)
    weather_today = db.Column(db.String(64))
    mood_today = db.Column(db.String(64))
    stress_level = db.Column(db.String(64))
    positive_affect_rating = db.Column(db.String(64))
    
    user = db.relationship('User', backref='daily_assessments')  # Use 'User' here

class Group(db.Model):
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.Text)

      # Define the many-to-many relationship with the User model
    members = db.relationship(
        'User',
        secondary=user_group_association,
        back_populates='groups'
    )
    def __init__(self, group_name, description):
        self.group_name = group_name
        self.description = description


class GroupPost(db.Model):
    __tablename__ = 'group_posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id'), nullable=False)
    post_content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Define the timestamp field

    # Define the relationships with the User and Group models
    user = db.relationship('User', backref='group_posts')
    group = db.relationship('Group', backref='group_posts')
    # Define the many-to-many relationship with the User model
 




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
    mood = db.relationship('Mood', back_populates='user_history_moods')
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
    user_history_moods = db.relationship('UserHistory', backref='mood_moods', lazy=True)

class Symptoms(db.Model):
    # Table contains information about other symptoms and is related to Coping Solutions.
    __tablename__ = 'symptoms'

    symptom_id = db.Column(db.Integer, primary_key=True)
    symptom_name = db.Column(db.String(255), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'), nullable=False)

    # Define the relationship with CopingSolution
    solution = db.relationship('CopingSolution', back_populates='symptoms')




def connect_db(app):
    """Connect this database to the provided Flask app.

    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)
    app.app_context().push()

    # Ensure that SQLAlchemy is properly configured
    mapper_registry.configure(db.metadata)

    # Create the database tables
    db.create_all()

