"""Model tests."""

# run these tests like:
#
#    python3 -m unittest Testing/test_models.py

import os
import unittest
from models import db, User, Group, GroupPost, Diagnosis, DiagnosisSolution, CopingSolution, UserDiagnosisAssociation, UserHistory,  JournalEntry, DailyAssessment, bcrypt
from datetime import datetime

# Set the database URL for testing
os.environ['DATABASE_URL'] = "postgresql:///moody"
from app import app

class UserDiagnosisAssociationModelTestCase(unittest.TestCase):
    """Test cases for the UserDiagnosisAssociation model."""
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # Create a user with user_id=2
        user = User(user_id=2, username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Create a diagnosis
        diagnosis = Diagnosis(issue_name='Test Diagnosis')
        db.session.add(diagnosis)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_create_user_diagnosis_association(self):
        # Retrieve the user with user_id=2
        user = User.query.get(2)

        # Retrieve the diagnosis with issue_name='Test Diagnosis'
        diagnosis = Diagnosis.query.filter_by(issue_name='Test Diagnosis').first()

        self.assertIsNotNone(user)
        self.assertIsNotNone(diagnosis)

        # Create a UserDiagnosisAssociation with the current date
        association = UserDiagnosisAssociation(
            user_id=user.user_id,
            diagnosis_id=diagnosis.issue_id,  # Assuming issue_id exists in the Diagnosis model
            date_recorded=datetime.utcnow().date()
        )
        db.session.add(association)
        db.session.commit()

        # Retrieve the association using filtering
        retrieved_association = UserDiagnosisAssociation.query.filter_by(
            user_id=user.user_id,
            diagnosis_id=diagnosis.issue_id
        ).first()

        self.assertIsNotNone(retrieved_association)
        self.assertIsNotNone(retrieved_association.date_recorded)
        self.assertEqual(retrieved_association.user_id, user.user_id)
        self.assertEqual(retrieved_association.diagnosis_id, diagnosis.issue_id)




class CopingSolutionModelTestCase(unittest.TestCase):
    """Test cases for the CopingSolution model."""
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # Create a CopingSolution instance
        coping_solution = CopingSolution(solution_text="Test Coping Solution")
        db.session.add(coping_solution)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_create_coping_solution(self):
        """Test creating a CopingSolution."""
        # Retrieve the CopingSolution with the solution text
        coping_solution = CopingSolution.query.filter_by(solution_text="Test Coping Solution").first()

        self.assertIsNotNone(coping_solution)

        retrieved_solution = CopingSolution.query.get(coping_solution.solution_id)

        self.assertEqual(retrieved_solution.solution_text, "Test Coping Solution")

    def test_coping_solution_users_relationship(self):
        """Test the relationship between CopingSolution and UserDiagnosisAssociation."""
        # Retrieve the UserDiagnosisAssociation with user_id=2 and diagnosis_id=2
        user_diagnosis = UserDiagnosisAssociation.query.filter_by(user_id=2, diagnosis_id=2).first()

        self.assertIsNotNone(user_diagnosis)

        self.assertIn(user_diagnosis, user_diagnosis.coping_solution_users)
        self.assertEqual(user_diagnosis.coping_solution, user_diagnosis.coping_solution)

class UserHistoryModelTestCase(unittest.TestCase):

    def setUp(self):
        # Create a user with a unique username
        unique_username = f"testuser_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        self.user = User(username=unique_username, email="test@test.com", password="testpassword")
        db.session.add(self.user)
        db.session.commit()

        # Create a Weather object
        weather = Weather(weather_date=datetime.utcnow().date(), temperature_value=25.0, temperature_unit="Celsius")
        db.session.add(weather)
        db.session.commit()

        # Create a UserHistory entry
        self.user_history = UserHistory(
            user_id=self.user.user_id,
            weather_id=weather.weather_id,  # Assign the weather_id
            date_recorded=datetime.utcnow().date()
        )
        db.session.add(self.user_history)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user_history(self):
        user_history = UserHistory.query.get(self.user_history.history_id)
        self.assertIsNotNone(user_history)
        self.assertEqual(user_history.user_id, self.user.user_id)

    def test_user_history_relationships(self):
        user_history = UserHistory.query.get(self.user_history.history_id)
        self.assertIsNotNone(user_history)
        self.assertEqual(user_history.user.username, "testuser")



