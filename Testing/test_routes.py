import unittest
import os
from datetime import datetime  # Add this line
from app import app, db
from models import User

# ... rest of your test code


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app since that will have already
# connected to the database)

os.environ['DATABASE_URL'] = "postgresql:///moody"

# Now we can import app

from app import app, CURR_USER_KEY, db

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data)

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class MoodyAppTestCase(unittest.TestCase):
    """Test cases for your Moody Flask app."""

    def setUp(self):
        """Set up the test environment."""
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG_TB_ENABLED'] = False

        self.client = app.test_client()

        with app.app_context():
            # Clean up existing test users with the same username
            existing_user = User.query.filter_by(username="testuser").first()
            if existing_user:
                db.session.delete(existing_user)
                db.session.commit()

            test_user = User.signup(
                username="testuser",
                email="test@test.com",
                password="testpassword",
                registration_date=datetime(2023, 10, 30, 14, 4, 25)
            )
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        """Tear down the test environment and the database."""
        with app.app_context():
            # Remove the test data
            test_user = User.query.filter_by(username="testuser").first()
            if test_user:
                db.session.delete(test_user)
                db.session.commit()

    def test_signup(self):
        """Test the user signup route."""

        with self.client as c:
            resp = c.post("/signup", data={
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword",
                "image_url": None
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Welcome! You have successfully signed up.", resp.data)

    def test_signup_existing_user(self):
        """Test signing up with an existing username."""

        with self.client as c:
            resp = c.post("/signup", data={
                "username": "testuser",
                "email": "test2@test.com",
                "password": "testuser",
                "image_url": None
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Username or email already taken", resp.data)

    def test_login(self):
        """Test the user login route."""

        with self.client as c:
            resp = c.post("/login", data={
                "username": "testuser",
                "password": "testpassword"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Hello, testuser!", resp.data)

    def test_logout(self):
        """Test the user logout route."""

        with self.client as c:
            resp = c.get("/logout", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"You have been logged out", resp.data)