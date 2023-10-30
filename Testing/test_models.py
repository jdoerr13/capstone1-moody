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

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.user = User.signup("testuser", "test@test.com", "password", None)
        db.session.add(self.user)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_create_user(self):
        """Test User.signup method."""
        user = User.signup(
            username="testuser2",
            email="test2@test.com",
            password="password",
            registration_date=datetime.utcnow()  # Provide a valid registration date
        )
        db.session.commit()
        retrieved_user = User.query.get(user.user_id)

        self.assertEqual(retrieved_user.username, "testuser2")

    def test_authenticate_valid_credentials(self):
        """Test User.authenticate method with valid credentials."""
        authenticated_user = User.authenticate("testuser", "password")

        self.assertEqual(authenticated_user.user_id, self.user.user_id)

    def test_password_hashing(self):
        """Test if the password is correctly hashed during user creation."""
        user = User.signup(
            username="testuser2",
            email="test2@test.com",
            password="password",
            registration_date=datetime.utcnow()
        )
        db.session.commit()

        # Verify that the stored password is a hash
        self.assertNotEqual(user.password, "password")

        # Verify that the password can be verified
        self.assertTrue(bcrypt.check_password_hash(user.password, "password"))

        # Verify that an incorrect password fails verification
        self.assertFalse(bcrypt.check_password_hash(user.password, "wrongpassword"))

class GroupModelTestCase(unittest.TestCase):
    """Test cases for the Group & GroupPost model."""
    def setUp(self):
        """Create a test client, add sample data, and create a test group."""
        db.drop_all()
        db.create_all()

        self.user = User.signup("testuser", "test@test.com", "password", None)
        db.session.add(self.user)

        # Create a test group
        self.group = Group(group_name="Test Group", description="This is a test group")
        db.session.add(self.group)

        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_create_group(self):
        """Test Group creation."""
        group = Group(group_name="New Group", description="This is a new group")
        db.session.add(group)
        db.session.commit()

        retrieved_group = Group.query.get(group.group_id)

        self.assertEqual(retrieved_group.group_name, "New Group")
        self.assertEqual(retrieved_group.description, "This is a new group")

    def test_group_relationships(self):
        """Test relationships of the Group model with other models."""
        # Create User and add it to the group
        user = User.signup("newuser", "new@test.com", "password", None)
        self.group.members.append(user)
        db.session.commit()

        # Check relationships
        self.assertIn(user, self.group.members)
        self.assertEqual(user.groups[0], self.group)
    
    def test_create_group_post(self):
        """Test creating a post within a group."""
        group_post = GroupPost(
            user_id=self.user.user_id,
            group_id=self.group.group_id,
            post_content="This is a test post in the group.",
        )
        db.session.add(group_post)
        db.session.commit()

        retrieved_post = GroupPost.query.get(group_post.id)

        self.assertEqual(retrieved_post.user_id, self.user.user_id)
        self.assertEqual(retrieved_post.group_id, self.group.group_id)
        self.assertEqual(retrieved_post.post_content, "This is a test post in the group.")

    def test_group_posts_relationship(self):
        """Test the relationship between Group and GroupPost."""
        group_post = GroupPost(
            user_id=self.user.user_id,
            group_id=self.group.group_id,
            post_content="A post in the group.",
        )
        db.session.add(group_post)
        db.session.commit()

        self.assertIn(group_post, self.group.group_posts)
        self.assertEqual(group_post.group, self.group)

class DiagnosisModelTestCase(unittest.TestCase):
    """Test cases for the Diagnosis model."""
    
    def setUp(self):
        """Create a test client, add sample data, and create a test group."""
        db.drop_all()
        db.create_all()

        # Create a user instance
        self.user = User.signup("testuser", "test@test.com", "password", datetime.utcnow())
        db.session.add(self.user)
        db.session.commit()

        # Create a diagnosis instance
        self.diagnosis = Diagnosis(issue_name="Test Diagnosis")
        db.session.add(self.diagnosis)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transactions and drop the test database."""
        db.session.remove()
        db.drop_all()

    def test_create_diagnosis(self):
        """Test creating a Diagnosis."""
        diagnosis = Diagnosis(issue_name="Another Diagnosis")
        db.session.add(diagnosis)
        db.session.commit()

        retrieved_diagnosis = Diagnosis.query.get(diagnosis.issue_id)

        self.assertEqual(retrieved_diagnosis.issue_name, "Another Diagnosis")

    def test_create_diagnosis_solution(self):
        # Create a valid CopingSolution first
        coping_solution = CopingSolution(solution_text="A valid solution")
        db.session.add(coping_solution)
        db.session.commit()

        # Create a DiagnosisSolution
        solution = DiagnosisSolution(
            user_id=self.user.user_id,
            diagnosis_id=self.diagnosis.issue_id,
            solution_id=coping_solution.solution_id,
            solution_text="A test solution for a diagnosis."
        )
        db.session.add(solution)
        db.session.commit()

        retrieved_solution = DiagnosisSolution.query.get(solution.id)
        self.assertEqual(retrieved_solution.solution_text, "A test solution for a diagnosis.")

    def test_diagnosis_solutions_relationship(self):
        """Test the relationship between Diagnosis and DiagnosisSolution."""
        # Create a valid CopingSolution first
        coping_solution = CopingSolution(solution_text="A valid solution")
        db.session.add(coping_solution)
        db.session.commit()

        # Create a DiagnosisSolution
        solution = DiagnosisSolution(
            user_id=self.user.user_id,
            diagnosis_id=self.diagnosis.issue_id,
            solution_id=coping_solution.solution_id,
            solution_text="A test solution for a diagnosis."
        )
        db.session.add(solution)
        db.session.commit()

        retrieved_diagnosis = Diagnosis.query.get(self.diagnosis.issue_id)
        self.assertIn(solution, retrieved_diagnosis.solutions)
        self.assertEqual(solution.diagnosis, retrieved_diagnosis)


class UserDiagnosisAssociationModelTestCase(unittest.TestCase):
    """Test cases for the UserDiagnosisAssociation model."""
    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        # Delete the existing user with the same username (if it exists)
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            db.session.delete(existing_user)
            db.session.commit()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()


    def test_create_user_diagnosis_association(self):
        # Create a user
        user = User(username='testuser', email='testuser@example.com', password='testpassword')
        db.session.add(user)
        db.session.commit()

        # Create a diagnosis
        diagnosis = Diagnosis(issue_name='Test Diagnosis')
        db.session.add(diagnosis)
        db.session.commit()

        # Create a UserDiagnosisAssociation with the current date
        association = UserDiagnosisAssociation(
            user_id=user.user_id,
            diagnosis_id=diagnosis.issue_id,
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
        self.coping_solution = CopingSolution(solution_text="Test Coping Solution")
        db.session.add(self.coping_solution)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transactions."""
        db.session.rollback()

    def test_create_coping_solution(self):
        """Test creating a CopingSolution."""
        coping_solution = CopingSolution(solution_text="Another Coping Solution")
        db.session.add(coping_solution)
        db.session.commit()

        retrieved_solution = CopingSolution.query.get(coping_solution.solution_id)

        self.assertEqual(retrieved_solution.solution_text, "Another Coping Solution")

    def test_coping_solution_users_relationship(self):
        """Test the relationship between CopingSolution and UserDiagnosisAssociation."""
        user_diagnosis = UserDiagnosisAssociation(user_id=1, diagnosis_id=1)
        db.session.add(user_diagnosis)
        db.session.commit()

        self.assertIn(user_diagnosis, self.coping_solution.users)
        self.assertEqual(user_diagnosis.coping_solution, self.coping_solution)





# Create separate test classes for other models (  UserHistory, JournalEntry, DailyAssessment) following a similar structure.

