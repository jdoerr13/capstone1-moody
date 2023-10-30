from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy instance
db = SQLAlchemy()

# Initialize Bcrypt for password hashing
bcrypt = Bcrypt()

# Define many-to-many association tables
user_group_association = db.Table(
    'user_group_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id')),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.group_id')),
    extend_existing=True,
)

user_friends = db.Table(
    'user_friends',
    db.Column('user_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)

user_friend_requests = db.Table(
    'user_friend_requests',
    db.Column('sender_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True),
    db.Column('receiver_id', db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
)

class UserDiagnosisAssociation(db.Model):
    __tablename__ = "user_diagnostic_ass"
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.issue_id'), primary_key=True)
    date_recorded = db.Column(db.Date, nullable=True)

    # Define the relationships with the User and Diagnosis models
    user = db.relationship('User', back_populates='diagnosis_associations')
    diagnosis = db.relationship('Diagnosis', back_populates='user_associations')

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)  
    bio = db.Column(db.Text)
    location = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    password = db.Column(db.String(120), nullable=False)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    user_histories = db.relationship('UserHistory', back_populates='user')
    solutions = db.relationship('DiagnosisSolution', back_populates='user')
    diagnosis_associations = db.relationship('UserDiagnosisAssociation', back_populates='user')

    friends = db.relationship(
        'User',
        secondary=user_friends,
        primaryjoin=(user_friends.c.user_id == user_id),
        secondaryjoin=(user_friends.c.friend_id == user_id),
        backref=db.backref('user_friends', lazy='dynamic'),
    )

    friend_requests = db.relationship(
        'User',
        secondary=user_friend_requests,
        primaryjoin=(user_friend_requests.c.sender_id == user_id),
        secondaryjoin=(user_friend_requests.c.receiver_id == user_id),
        backref=db.backref('user_friend_requests', lazy='dynamic'),
    )

    groups = db.relationship(
        'Group',
        secondary=user_group_association,
        back_populates='members',
    )

    @classmethod
    def signup(cls, username, email, password, registration_date):
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

class UserHistory(db.Model):
    __tablename__ = 'user_history'

    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    weather_id = db.Column(db.Integer, db.ForeignKey('weather.weather_id'), nullable=False)
    date_recorded = db.Column(db.Date, nullable=False, unique=True)  # Add a unique constraint

    user = db.relationship('User', back_populates='user_histories')
    weather = db.relationship('Weather', back_populates='user_history')




class DiagnosisSolution(db.Model):
    __tablename__ = 'diagnosis_solutions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))  # Add this line
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis.issue_id'))
    solution_id = db.Column(db.Integer, db.ForeignKey('coping_solutions.solution_id'))
    solution_text = db.Column(db.Text)

    user = db.relationship('User', back_populates='solutions')
    diagnosis = db.relationship('Diagnosis', back_populates='solutions')
    solution = db.relationship('CopingSolution', back_populates='diagnoses')


# Define Diagnosis
class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'

    issue_id = db.Column(db.Integer, primary_key=True)
    issue_name = db.Column(db.String(255), nullable=False)

    solutions = db.relationship('DiagnosisSolution', back_populates='diagnosis')
    user_associations = db.relationship('UserDiagnosisAssociation', back_populates='diagnosis')

# Define CopingSolution
class CopingSolution(db.Model):
    __tablename__ = 'coping_solutions'

    solution_id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False)

    diagnoses = db.relationship('DiagnosisSolution', back_populates='solution')

# Define JournalEntry
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

class DailyAssessment(db.Model):
    __tablename__ = 'daily_assessment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.Date)
    weather_today = db.Column(db.String(64))
    mood_today = db.Column(db.String(64))
    stress_level = db.Column(db.Text)
    positive_affect_rating = db.Column(db.Text)

    user = db.relationship('User', backref='daily_assessments')

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





def connect_db(app):
    """Connect this database to the provided Flask app.

    all this in your Flask app.
    """
    db.app = app
    db.init_app(app)
    app.app_context().push()


    # Create the database tables
    db.create_all()

