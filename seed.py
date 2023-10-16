"""Seed database with sample data for Groups."""
from app import db
from models import Group

def seed_groups():
    # Create instances for each group
    group1 = Group(group_name="Climate Change Anxiety", description="Group for climate change-related discussions.")
    group2 = Group(group_name="Extreme Weather or Major Disaster", description="Group for extreme weather and disaster discussions.")
    group3 = Group(group_name="Weather makes me moody", description="Group for discussing mood and weather correlations.")
    group4 = Group(group_name="SAD", description="Group for Seasonal Affective Disorder (SAD) support.")
    group5 = Group(group_name="General Weather Stress", description="Group for general weather-related stress discussions.")

    # Add the groups to the database
    db.session.add(group1)
    db.session.add(group2)
    db.session.add(group3)
    db.session.add(group4)
    db.session.add(group5)

    # Commit the changes to the database
    db.session.commit()

if __name__ == "__main__":
    # Initialize your Flask app and configure it, if necessary
    # Example: from app import app
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-connection-string'

    # Run the seed function
    seed_groups()