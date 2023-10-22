from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, TextAreaField, RadioField, SelectMultipleField, widgets, BooleanField, SubmitField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, InputRequired, Optional
from models import User, bcrypt
from flask import g
from datetime import datetime
from wtforms.widgets import ListWidget, CheckboxInput
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Signup form."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6), DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password', message='Passwords must match'), DataRequired()])
    submit = SubmitField('Sign Up')

    # Custom validator to check if the username is already taken
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

    # Custom validator to check if the email is already registered
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

class JournalEntryForm(FlaskForm):
    entry_id = HiddenField('Entry ID')  # Hidden field for the entry ID
    date = DateField('Date', validators=[DataRequired()])
    entry = TextAreaField('Journal Entry', validators=[DataRequired()])

# class DailyMoodForm(FlaskForm):

class MoodSymptomAssessmentForm(FlaskForm):
    weather_today = SelectMultipleField('1. How is the weather today? (Select all that apply)', 
                                       choices=[
                                           ('sunny', 'Sunny'),
                                           ('cloudy', 'Cloudy'),
                                           ('rainy', 'Rainy'),
                                           ('windy', 'Windy'),
                                           ('partly_cloudy', 'Partly Cloudy'),
                                           ('stormy', 'Stormy'),
                                           ('foggy', 'Foggy'),
                                           ('snowy', 'Snowy'),
                                           ('hot', 'Hot'),
                                           ('cold', 'Cold')
                                       ],
                                       widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())

    mood_today = SelectMultipleField('2. How are you feeling today? (Select all that apply)', choices=[
   ('happy', '1 - Happy'),
    ('sad', '2 - Sad'),
    ('angry', '3 - Angry'),
    ('neutral', '4 - Neutral'),
    ('energetic', '5 - Energetic'),
    ('anxious', '6 - Anxious'),
    ('content', '7 - Content'),
    ('irritable', '8 - Irritable'),
    ('confident', '9 - Confident'),
    ('relaxed', '10 - Relaxed'),
    ('stressed', '11 - Stressed'),
    ('focused', '12 - Focused'),
    ('blam Moody', '13 - Bla Moody'),
    ('below Average', '14 - Below Average'),
    ('moderate/mellow', '15 - Moderate/Mellow'),
    ('above Average', '16 - Above Average'),
    ('pretty Good!', '17 - Pretty Good!'),
    ('feeling Good!', '18 - Feeling Good!'),
    ('great', '19 - Great'),
    ('very happy and/or Excited', '20 - Very happy and/or Excited')
    ])
    
    stress_level = RadioField('3. On a scale of 1-10, how would you rate your stress level today?', choices=[
        ('1', '1 - Very low'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10 - Very high')
    ])

    positive_affect_rating = RadioField('4. How is your mood today on a scale from 1-10? where 1 means you are feeling very low/sad, and 10 means you are feeling very happy/positive.', choices=[
    ('1', '1 - Very low'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10 - Very high')
    ])

    positive_affect_threshold = RadioField('5. Do you think that feeling happy or positive is more affected by the weather than feeling sad or negative? Choose "Yes" if you think it is easier, "No" if you think it is about the same, or "Not sure" if you are unsure.', choices=[('yes', 'Yes'), ('no', 'No'), ('not_sure', 'Not sure')])

    climate_anxiety = RadioField('6. Have you ever dealt with climate change anxiety?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    mood_swings_weather = RadioField('7. Do you experience mood swings due to weather changes?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    experienced_sad_disaster = RadioField('8. Have you ever dealt with mood changes due to a major disaster or extreme weather conditions?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    primary_purpose = RadioField('9. What is your primary purpose for joining this app?', choices=[('meet_friends', 'Meet Friends'), ('learn_more_about_myself', 'Learn More About Myself'), ('improve_moods', 'Improve My Moods'), ('just_curious', 'Just Curious')], validators=[InputRequired()])

    mood_variation_weather = RadioField('10. Do you notice mood variations on different types of weather days, such as "nice days" and "poor weather days"?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    variations = TextAreaField('11. If you answered "Yes" to the previous question, what weather condition(s) affect you positively & negatively?', validators=[Length(max=1000)])

    weather_mood_beliefs = RadioField('12. Do you believe that your mood is influenced by specific weather conditions?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    impact_behavior = RadioField('13. Have you noticed any changes in your behavior due to specific weather conditions?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    behavioral_changes = TextAreaField('14. If you answered "Yes" to the previous question, please describe some specific behavioral changes you\'ve noticed in response to certain weather conditions.', validators=[Length(max=1000)])

    experienced_sad = RadioField('15. Do you usually feel down on rainy or cloudy days?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    experienced_happy = RadioField('16. Do you usually feel happy on sunny days?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    seasonal_affective_disorder = RadioField('17. Have you ever experienced symptoms related to Seasonal Affective Disorder (SAD)?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])


    weather_variables = SelectMultipleField('18. Have you observed mood changes linked to specific weather variables? (Select all that apply)', choices=[
        ('temperature', 'Temperature'),
        ('humidity', 'Humidity'),
        ('precipitation', 'Precipitation'),
        ('barometric_pressure', 'Barometric Pressure'),
        ('wind_speed', 'Wind Speed'),
        ('sunlight', 'Sunlight'),
        ('uv_index', 'UV Index'),
        ('pollution_levels', 'Pollution Levels'),
        ('seasonal_changes', 'Seasonal Changes')
    ])


    number_18 = TextAreaField('19. If yes for #18, please discribe')

    sleep_hours = RadioField('20. How many hours of sleep did you get last night?', choices=[
        ('0-4', '0-4 hours'),
        ('5-7', '5-7 hours'),
        ('8-10', '8-10 hours'),
        ('10+', 'More than 10 hours')
    ])

    exercise = RadioField('21. Did you engage in physical exercise today?', choices=[
        ('yes', 'Yes'),
        ('no', 'No')
    ])
    exercise_description = StringField('22. If yes, please describe the type and duration of exercise')

    exercise_frequency = RadioField('23. How often do you exercise?', choices=[
        ('rarely', 'Rarely'),
        ('once a week', 'Once a week'),
        ('several times a week', 'Several times a week'),
        ('daily', 'Daily')
    ])

    future_research_weather_variables = RadioField('24. How would you propose studying the effects of a broader range of weather and seasonal variables on mood?', choices=[
        ('broaden_variables', 'Broaden the range of variables studied'),
        ('focus_on_specifics', 'Focus on specific weather variables'),
        ('other', 'Other'),
        ('not_sure', 'Not Sure')
    ])
    geographic_duration = RadioField('25. How long have you lived in your current geographic location?', choices=[
        ('less_than_1_year', 'Less than a year'),
        ('1-5_years', '1-5 years'),
        ('5-10_years', '5-10 years'),
        ('more_than_10_years', 'More than 10 years')
    ])

    experienced_geographic_changes = RadioField('26. Have you experienced seasonal mood changes based on your geographic location?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    geographic_location = RadioField('27. Have you ever relocated to a different geographical location for better weather?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    impact_relocation = RadioField('28. If you have relocated, have you noticed changes in your mood related to the novel weather conditions in your new location?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    relocate_changes = TextAreaField('29. If you answered "Yes" to the previous question, please describe.', validators=[Length(max=1000)])

    other_factors_influence_mood = SelectMultipleField('30. What other factors, apart from weather, do you believe influence your mood on a daily basis?', 

    choices=[
        ('academic_or_work', 'Academic or work-related factors'),
        ('personal_relationships', 'Personal relationships'),
        ('health_and_well_being', 'Health and well-being'),
        ('other', 'Other')
    ],
      widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())

   
    other_factors_description = TextAreaField('31. If you selected "Other" in the previous question, please specify what other factors influence your mood.')

    diet_influence = RadioField('32. Do you notice changes in your eating habits or food preferences based on the weather?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    diet_changes_description = TextAreaField('33. If you experience changes in your eating habits based on the weather, please describe them.', validators=[Length(max=1000)])

    physical_symptoms = SelectMultipleField('34. Please check any physical symptoms you have experienced due to weather conditions:', 
    
            choices = [
        ('headache', 'Headache'),
        ('joint_pain', 'Joint Pain'),
        ('migraine', 'Migraine'),
        ('sinus_congestion', 'Sinus Congestion'),
        ('fatigue', 'Fatigue'),
        ('nausea', 'Nausea'),
        ('allergies', 'Allergies'),
        ('sore_throat', 'Sore Throat'),
        ('stiffness', 'Stiffness'),
        ('shortness_of_breath', 'Shortness of Breath'),
        ('other', 'Other')
    ])
     

    physical_symptoms_description = TextAreaField('35. If you experience physical symptoms related to weather, please describe the related weather conditions in addition to any other symptoms not included above.', validators=[Length(max=1000)])

    outdoor_activities = RadioField('36. Do you engage in outdoor activities and notice physical or mental changes based on the weather?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    outdoor_activities_description = TextAreaField('37. If you engage in outdoor activities and weather affects them, was it physical, mental, or both?', validators=[Length(max=1000)])

    social_interaction = RadioField('38. Do you find that your social interactions change based on the weather?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    social_interaction = RadioField('39. Do you often find yourself feeling overwhelmed, anxious, or stressed when thinking about or experiencing the effects of climate change or environmental issues?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])


    emotional_support = RadioField('40. Do you seek emotional support from friends or family when your mood is affected by the weather?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    estorms = RadioField('41. Do you worry about the possibility of major disasters or severe weather events affecting your life or community, even when there is no imminent threat?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[InputRequired()])

    coping_strategies = TextAreaField('42. Do you have specific strategies or activities to cope with weather-related mood and symptom changes?', validators=[Length(max=1000)])

    long_term_patterns = TextAreaField('43. Have you noticed any long-term patterns or trends in how weather affects your mood and symptoms?', validators=[Length(max=1000)])

    emotional_support_description = TextAreaField('44. If you seek emotional support related to weather, please describe who you turn to and why. (optional)', validators=[Length(max=1000)])

    expectations_beliefs = TextAreaField('45. Do you have beliefs or expectations about how specific weather conditions affect your mood? (optional)', validators=[Length(max=1000)])

    additional_comments = TextAreaField('46. Do you have any additional comments or observations about your mood or symptoms? (optional)')

    importance_of_survey_time = RadioField('47. How important do you think it is to complete mood surveys at the same time each day for accurate assessment? (optional)', choices=[
        ('very important', 'Very Important'),
        ('somewhat important', 'Somewhat Important'),
        ('not very important', 'Not Very Important')
    ])

    future_research_time = StringField('47. What are some specific recommendations for improving future research on the weather-mood relationship? (optional)', validators=[Length(max=1000)])


class DailyAssessmentForm(FlaskForm):
    weather_today = SelectMultipleField('1. How is the weather today? (Select all that apply)', 
                                       choices=[
                                           ('sunny', 'Sunny'),
                                           ('cloudy', 'Cloudy'),
                                           ('rainy', 'Rainy'),
                                           ('windy', 'Windy'),
                                           ('partly_cloudy', 'Partly Cloudy'),
                                           ('stormy', 'Stormy'),
                                           ('foggy', 'Foggy'),
                                           ('snowy', 'Snowy'),
                                           ('hot', 'Hot'),
                                           ('cold', 'Cold')
                                       ],
                                       widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())

    mood_today = SelectMultipleField('2. How are you feeling today? (Select all that apply)', choices=[
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('neutral', 'Neutral'),
        ('energetic', 'Energetic'),
        ('anxious', 'Anxious'),
        ('content', 'Content'),
        ('irritable', 'Irritable'),
        ('confident', 'Confident'),
        ('relaxed', 'Relaxed'),
        ('stressed', 'Stressed')
    ])
    
    stress_level = SelectMultipleField('3. On a scale of 1-10, how would you rate your stress level today?', choices=[
        ('1', '1 - Very low'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10 - Very high')
    ])

    positive_affect_rating = SelectMultipleField('4. How is your mood today on a scale from 1-10? where 1 means you are feeling very low/sad, and 10 means you are feeling very happy/positive.', choices=[
        ('1', '1 - Very low'),
        ('2', '2 - Low'),
        ('3', '3 - Bla Moody'),
        ('4', '4 - Below Average'),
        ('5', '5 - moderate/mellow'),
        ('6', '6 - Above Average'),
        ('7', '7 - Pretty Good!'),
        ('8', '8 - Feeling Good!'),
        ('Great!', '9 - Great!'),
        ('Very happy and/or Excited', '10 - Very happy and/or Excited')
    ])



class ProfileEditForm(FlaskForm):
    """Form for editing user profile."""

    username = StringField('Username', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    bio = TextAreaField('Bio', validators=[Optional()])
    location = StringField('Location (City, State)', validators=[Optional()], default="Default City, State")
    image_url = StringField('Profile Picture', validators=[Optional()])
    
    current_password = PasswordField('Current Password', validators=[DataRequired()])
 

    def validate_password(self, field):
        # Check if the entered password matches the user's current password
        user = User.query.get_or_404(g.user.user_id)  # Assuming g.user is the current user

        if not bcrypt.check_password_hash(user.password, field.data):
            raise ValidationError('Incorrect password')