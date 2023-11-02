import unittest
import os
from app import app, db, CURR_USER_KEY
from models import User
from flask import session
from forms import bcrypt


os.environ['DATABASE_URL'] = "postgresql:///moody"


app.config['WTF_CSRF_ENABLED'] = False


class MoodyAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        db.session.rollback()
        app.config['TESTING'] = False

    def login_user(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1  # Replace with an actual user ID
        return c

    def test_signup(self):
        response = self.client.post('/signup', data=dict(
            username='testuser',
            email='test@test.com',
            password='password'
        ), follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Create a user for testing
        user = User.signup('testuser', 'test@test.com', 'password', None)
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data=dict(
            username='testuser',
            password='password'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, testuser!', response.data)

    def test_logout(self):
        # Create a user for testing
        user = User.signup('testuser', 'test@test.com', 'password', None)
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with self.client as c:
            c.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)

            response = c.get('/logout', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'You have been logged out', response.data)

    def test_current(self):
        response = self.client.post('/current', data=dict(
            location='New York, NY'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_forecast(self):
        response = self.client.post('/forecast', data=dict(
            location='Boca Raton, FL'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_astronomy(self):
        response = self.client.post('/astronomy', data=dict(
            location='New York',
            date='2023-10-25'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_set_location(self):
        # Create a user for testing
        user = User.signup('testuser', 'test@test.com', 'password', None)
        db.session.add(user)
        db.session.commit()

        # Log in the user
        with self.client as c:
            c.post('/login', data=dict(
                username='testuser',
                password='password'
            ), follow_redirects=True)

            response = c.post('/set_location', data=dict(
                location='New York'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Location and weather data updated successfully!', response.data)

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Greetings New Friend', response.data)
        self.assertIn(b'New to Moody?', response.data)
        self.assertIn(b'Sign up now to meet other moodies', response.data)
        self.assertIn(b'Sign up', response.data)

    def test_edit_profile(self):
        with self.login_user():
            response = self.client.get('/edit_profile', follow_redirects=True)
            self.assertEqual(response.status_code, 200)

    # def test_uploaded_file(self):
    #     # Simulate a GET request to the '/uploads/<filename>' route
    #     response = self.client.get('/uploads/test.jpg')
    #     self.assertEqual(response.status_code, 200)


    def set_up_valid_user_session(self, user_id):
        with self.client.session_transaction() as sess:
            sess[CURR_USER_KEY] = user_id

    def test_friends_profile(self):
        # Ensure that the user with user_id 1 exists in your test database
        # Create and add the test user to the database
        test_user = User(user_id=1, username='testuser', email='test@example.com')
        test_user.password = bcrypt.generate_password_hash('password').decode('utf-8')  # Replace 'password' with the actual password
        # You may set other attributes as needed
        db.session.add(test_user)
        db.session.commit()

        # Set up a valid user session
        user_id = 1  # User with user_id 1
        self.set_up_valid_user_session(user_id)

        # Make the request to the friends_profile route
        response = self.client.get('/friends_profile/1')  # Replace with a valid user_id

        self.assertEqual(response.status_code, 200)

    def test_send_friend_request(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 1  # Replace with a valid user ID
            response = c.post('/send_friend_request/2')  # Replace with a valid user_id
            self.assertEqual(response.status_code, 200)  # Check if the user is logged in

    def test_accept_friend_request(self):
        response = self.client.post('/accept_friend_request/2')
        self.assertEqual(response.status_code, 200)

    def test_remove_friend(self):
        # Ensure a user is logged in
        self.login_user()
        
        # Simulate a POST request to the '/remove_friend/<int:friend_id>' route
        response = self.client.post('/remove_friend/3')  # Replace with a valid friend_id

        # Check if the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 302)

        # Optionally, you can check the location where the redirect points to
        self.assertIn('/friends_groups', response.location)


    def test_mood_symptom(self):
        with self.client:
            response = self.client.get('/mood_symptom')
            self.assertEqual(response.status_code, 200)

    def test_diagnosis_history(self):
        response = self.client.get('/diagnosis_history')
        self.assertEqual(response.status_code, 200)

    def test_daily_assessment(self):
        response = self.client.get('/daily_assessment')
        self.assertEqual(response.status_code, 200)




