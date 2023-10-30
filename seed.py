import os
from app import app, db  # Import your Flask app and SQLAlchemy instance
from models import Group, Diagnosis, CopingSolution, DiagnosisSolution

def seed_groups():
    # Create instances for each group
    group1 = Group(group_name="Climate Change Anxiety", description="Group for climate change-related discussions.")
    group2 = Group(group_name="Major Disaster/Severe Weather Anxiety", description="Group for extreme weather and disaster discussions.")
    group3 = Group(group_name="Weather makes me moody", description="Group for discussing mood and weather correlations.")
    group4 = Group(group_name="SAD", description="Group for Seasonal Affective Disorder (SAD) support.")
    group5 = Group(group_name="General Weather Stress/ Cabin Fever", description="Group for general weather-related stress discussions.")
    group6 = Group(group_name="Weather & Physical Health", description="Weather & Physical Health")

    # Add the groups to the database
    db.session.add_all([group1, group2, group3, group4, group5, group6])
    db.session.commit()

def seed_diagnoses():
    # Create instances for each diagnosis
    diagnosis1 = Diagnosis(issue_name="Climate Change or Environmental Anxiety")
    diagnosis2 = Diagnosis(issue_name="Major Disaster or Severe Weather Anxiety")
    diagnosis3 = Diagnosis(issue_name="Weather-Induced Mood Swings (Moody)")
    diagnosis4 = Diagnosis(issue_name="Seasonal Affective Disorder (SAD)")
    diagnosis5 = Diagnosis(issue_name="General Weather Stress or Cabin Fever")
    diagnosis6 = Diagnosis(issue_name="Weather-Induced Physical Issues")

    # Add the diagnoses to the database
    db.session.add_all([diagnosis1, diagnosis2, diagnosis3, diagnosis4, diagnosis5, diagnosis6])
    db.session.commit()

def seed_coping_solutions():
    # Create instances for coping solutions
    solution1 = CopingSolution(solution_text="Stay informed about climate issues and actions you can take.")
    solution2 = CopingSolution(solution_text="Practice eco-friendly habits to reduce personal environmental impact.")
    solution3 = CopingSolution(solution_text="Seek professional therapy to address anxiety and fears related to climate change.")
    solution4 = CopingSolution(solution_text="Create an emergency plan for your family and home.")
    solution5 = CopingSolution(solution_text="Stay informed about disaster preparedness and local resources.")
    solution6 = CopingSolution(solution_text="Consider professional therapy to address disaster-related anxiety.")
    solution7 = CopingSolution(solution_text="Monitor weather forecasts and plan activities accordingly.")
    solution8 = CopingSolution(solution_text="Engage in mood-boosting activities on gloomy days.")
    solution9 = CopingSolution(solution_text="Consider therapy to manage mood swings influenced by the weather.")
    solution10 = CopingSolution(solution_text="Use light therapy to mitigate the effects of reduced daylight.")
    solution11 = CopingSolution(solution_text="Stay active and maintain a consistent daily routine.")
    solution12 = CopingSolution(solution_text="Consult a mental health professional for SAD-specific therapies.")
    solution13 = CopingSolution(solution_text="Engage in indoor hobbies or activities during poor weather.")
    solution14 = CopingSolution(solution_text="Practice relaxation techniques to reduce stress and cabin fever.")
    solution15 = CopingSolution(solution_text="Seek therapy for managing stress and coping with weather-induced stress.")
    solution16 = CopingSolution(solution_text="Monitor your physical symptoms and seek medical advice as needed.")
    solution17 = CopingSolution(solution_text="Stay active and maintain a healthy lifestyle regardless of the weather.")
    solution18 = CopingSolution(solution_text="Consult healthcare professionals for addressing weather-induced physical issues.")

    # Add the coping solutions to the database
    db.session.add_all([solution1, solution2, solution3, solution4, solution5, solution6,
                        solution7, solution8, solution9, solution10, solution11, solution12,
                        solution13, solution14, solution15, solution16, solution17, solution18])
    db.session.commit()

def seed_diagnosis_solutions():
    # Add records to link diagnoses and coping solutions
    # You can use the following format: (diagnosis_id, solution_id)
    records = [
        (1, 1), (1, 2), (1, 3),
        (2, 4), (2, 5), (2, 6),
        (3, 7), (3, 8), (3, 9),
        (4, 10), (4, 11),
 ]

    # Create instances for diagnosis solutions
    for record in records:
        diagnosis_solution = DiagnosisSolution(diagnosis_id=record[0], solution_id=record[1])
        db.session.add(diagnosis_solution)

    # Commit changes
    db.session.commit()

def update_diagnosis_solution_text():
    # Update solution_text in diagnosis_solutions based on coping_solutions
    db.session.execute(
        '''
        UPDATE diagnosis_solutions AS ds
        SET solution_text = cs.solution_text
        FROM coping_solutions AS cs
        WHERE ds.solution_id = cs.solution_id;
        '''
    )
    db.session.commit()

if __name__ == "__main__":
    # Configure your app and database connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///moody')

    with app.app_context():
        # Run the seed functions
        seed_groups()
        seed_diagnoses()
        seed_coping_solutions()
        seed_diagnosis_solutions()
        update_diagnosis_solution_text()


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






# if __name__ == "__main__":
#     # Configure your app and database connection string
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///moody')

#     # Run the seed functions
#     seed_diagnoses()
#     seed_coping_solutions()









# INSERT INTO groups (group_name, description) VALUES
# ('Climate Change Anxiety', 'Group for climate change-related discussions.'),
# ('Major Disaster/Severe Weather Anxiety', 'Group for extreme weather and disaster discussions.'),
# ('Weather makes me moody', 'Group for discussing mood and weather correlations.'),
# ('SAD', 'Group for Seasonal Affective Disorder (SAD) support.'),
# ('General Weather Stress/ Cabin Fever', 'Group for general weather-related stress discussions.'),
# ('Weather & Physical Health', 'Weather & Physical Health');


# moody=# select * from coping_solutions;
#  solution_id |                                   solution_text                                   
# -------------+-----------------------------------------------------------------------------------
#            1 | Stay informed about climate issues and actions you can take.
#            2 | Practice eco-friendly habits to reduce personal environmental impact.
#            3 | Seek professional therapy to address anxiety and fears related to climate change.
#            4 | Create an emergency plan for your family and home.
#            5 | Stay informed about disaster preparedness and local resources.
#            6 | Consider professional therapy to address disaster-related anxiety.
#            7 | Monitor weather forecasts and plan activities accordingly.
#            8 | Engage in mood-boosting activities on gloomy days.
#            9 | Consider therapy to manage mood swings influenced by the weather.
#           10 | Use light therapy to mitigate the effects of reduced daylight.
#           11 | Stay active and maintain a consistent daily routine.
#           12 | Consult a mental health professional for SAD-specific therapies.
#           13 | Engage in indoor hobbies or activities during poor weather.
#           14 | Practice relaxation techniques to reduce stress and cabin fever.
#           15 | Seek therapy for managing stress and coping with weather-induced stress.
#           16 | Monitor your physical symptoms and seek medical advice as needed.
#           17 | Stay active and maintain a healthy lifestyle regardless of the weather.
#           18 | Consult healthcare professionals for addressing weather-induced physical issues.
# (18 rows)

# moody=# select * from diagnosis;                                                 issue_id |                issue_name                
# ----------+------------------------------------------
#         1 | Climate Change or Environmental Anxiety
#         2 | Major Disaster or Severe Weather Anxiety
#         3 | Weather-Induced Mood Swings (Moody)
#         4 | Seasonal Affective Disorder (SAD)
#         5 | General Weather Stress or Cabin Fever
#         6 | Weather-Induced Physical Issues


# moody=# SELECT * FROM diagnosis_solutions;
#  id | diagnosis_id | solution_id 
# ----+--------------+-------------
#   1 |            1 |           1
#   2 |            1 |           2
#   3 |            1 |           3
#   7 |            2 |           4
#   8 |            2 |           5
#   9 |            2 |           6
#  13 |            3 |           7
#  14 |            3 |           8
#  15 |            3 |           9
#  19 |            4 |          10
#  20 |            4 |          11
#  21 |            4 |          12
#  25 |            5 |          13
#  26 |            5 |          14
#  27 |            5 |          15
#  31 |            6 |          16
#  32 |            6 |          17
#  33 |            6 |          18
# (18 rows)
 

#  then: -- 
# Update solution_text in diagnosis_solutions table based on coping_solutions

# UPDATE diagnosis_solutions AS ds
# SET solution_text = cs.solution_text
# FROM coping_solutions AS cs
# WHERE ds.solution_id = cs.solution_id;