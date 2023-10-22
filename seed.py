# Import the necessary modules
from app import app, db
from models import Group, Diagnosis, CopingSolution
import os

# def seed_groups():
#     # Create instances for each group
#     group1 = Group(group_name="Climate Change Anxiety", description="Group for climate change-related discussions.")
#     group2 = Group(group_name="Major Disaster/Severe Weather Anxiety", description="Group for extreme weather and disaster discussions.")
#     group3 = Group(group_name="Weather makes me moody", description="Group for discussing mood and weather correlations.")
#     group4 = Group(group_name="SAD", description="Group for Seasonal Affective Disorder (SAD) support.")
#     group5 = Group(group_name="General Weather Stress/ Cabin Fever", description="Group for general weather-related stress discussions.")
#     group6 = Group(group_name="Weather & Physical Health", description="Weather & Physical Health")

#     Add the groups to the database
#     db.session.add(group1)
#     db.session.add(group2)
#     db.session.add(group3)
#     db.session.add(group4)
#     db.session.add(group5)
#     db.session.add(group6)
#     db.session.commit()

def seed_diagnoses():
    # Create instances for each diagnosis and their corresponding solution_ids
    diagnoses_data = [
        ("Climate Change or Environmental Anxiety", "Stay informed about climate issues and actions you can take."),
        ("Major Disaster or Severe Weather Anxiety", "Create an emergency plan for your family and home."),
        ("Weather-Induced Mood Swings (Moody)", "Monitor weather forecasts and plan activities accordingly."),
        ("Seasonal Affective Disorder (SAD)", "Use light therapy to mitigate the effects of reduced daylight."),
        ("General Weather Stress or Cabin Fever", "Engage in indoor hobbies or activities during poor weather."),
        ("Weather-Induced Physical Issues", "Monitor your physical symptoms and seek medical advice as needed."),
    ]

    # Get the solution dictionary
    solution_dict = seed_coping_solutions()

    # Add the diagnoses to the database
    for issue_name, solution_text in diagnoses_data:
        diagnosis = Diagnosis(issue_name=issue_name, solution_id=solution_dict[solution_text])
        db.session.add(diagnosis)

    # Commit the changes to the database
    db.session.commit()


def seed_coping_solutions():
    # Create instances for coping solutions
    solutions = [
        # For Climate Change or Environmental Anxiety
        "Stay informed about climate issues and actions you can take.",
        "Practice eco-friendly habits to reduce personal environmental impact.",
        "Seek professional therapy to address anxiety and fears related to climate change.",

        # For Major Disaster or Severe Weather Anxiety
        "Create an emergency plan for your family and home.",
        "Stay informed about disaster preparedness and local resources.",
        "Consider professional therapy to address disaster-related anxiety.",

        # For Weather-Induced Mood Swings (Moody)
        "Monitor weather forecasts and plan activities accordingly.",
        "Engage in mood-boosting activities on gloomy days.",
        "Consider therapy to manage mood swings influenced by the weather.",

        # For Seasonal Affective Disorder (SAD)
        "Use light therapy to mitigate the effects of reduced daylight.",
        "Stay active and maintain a consistent daily routine.",
        "Consult a mental health professional for SAD-specific therapies.",

        # For General Weather Stress or Cabin Fever
        "Engage in indoor hobbies or activities during poor weather.",
        "Practice relaxation techniques to reduce stress and cabin fever.",
        "Seek therapy for managing stress and coping with weather-induced stress.",

        # For Weather-Induced Physical Issues
        "Monitor your physical symptoms and seek medical advice as needed.",
        "Stay active and maintain a healthy lifestyle regardless of the weather.",
        "Consult healthcare professionals for addressing weather-induced physical issues."
    ]

    solution_dict = {}  # Create a dictionary to store solutions and their IDs

    for solution_text in solutions:
        solution = CopingSolution(solution_text=solution_text)
        db.session.add(solution)
        db.session.flush()  # Flush to get the generated solution_id
        db.session.commit()  # Commit the solution to the database

        solution_dict[solution_text] = solution.solution_id

    return solution_dict  # Return the dictionary

if __name__ == "__main__":
    # Configure your app and database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///moody')

    # Run the seed functions
    seed_diagnoses()
    seed_coping_solutions()
