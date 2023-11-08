import os
from app import app, db  
from models import Group, Diagnosis, CopingSolution, DiagnosisSolution

# db.drop_all()
# db.create_all()

def seed_data():
    with app.app_context():

        print("Clearing old data...")
        Group.query.delete()
        Diagnosis.query.delete()
        CopingSolution.query.delete()
        DiagnosisSolution.query.delete()

# Create and commit instances for each group
        print("Seeding groups...")
        groups = [
            Group(group_name="Climate Change Anxiety", description="Group for climate change-related discussions."),
            Group(group_name="Major Disaster/Severe Weather Anxiety", description="Group for extreme weather and disaster discussions."),
            Group(group_name="Weather makes me moody", description="Group for discussing mood and weather correlations."),
            Group(group_name="SAD", description="Group for Seasonal Affective Disorder (SAD) support."),
            Group(group_name="General Weather Stress/ Cabin Fever", description="Group for general weather-related stress discussions."),
            Group(group_name="Weather & Physical Health", description="Weather & Physical Health"),
        ]

 
        db.session.bulk_save_objects(groups)
        db.session.commit()

# Create and commit instances for each diagnosis
        print("Seeding diagnoses...")
        diagnoses = [
            Diagnosis(issue_name="Climate Change or Environmental Anxiety"),
            Diagnosis(issue_name="Major Disaster or Severe Weather Anxiety"),
            Diagnosis(issue_name="Weather-Induced Mood Swings (Moody)"),
            Diagnosis(issue_name="Seasonal Affective Disorder (SAD)"),
            Diagnosis(issue_name="General Weather Stress or Cabin Fever"),
            Diagnosis(issue_name="Weather-Induced Physical Issues"),
        ]

        db.session.bulk_save_objects(diagnoses)
        db.session.commit()

# Create and commit instances for coping solutions
        print("Seeding coping solutions...")
        coping_solutions = [
            CopingSolution(solution_text="Stay informed about climate issues and actions you can take."),
            CopingSolution(solution_text="Practice eco-friendly habits to reduce personal environmental impact."),
            CopingSolution(solution_text="Seek professional therapy to address anxiety and fears related to climate change."),
            CopingSolution(solution_text="Create an emergency plan for your family and home."),
            CopingSolution(solution_text="Stay informed about disaster preparedness and local resources."),
            CopingSolution(solution_text="Consider professional therapy to address disaster-related anxiety."),
            CopingSolution(solution_text="Monitor weather forecasts and plan activities accordingly."),
            CopingSolution(solution_text="Engage in mood-boosting activities on gloomy days."),
            CopingSolution(solution_text="Consider therapy to manage mood swings influenced by the weather."),
            CopingSolution(solution_text="Use light therapy to mitigate the effects of reduced daylight."),
            CopingSolution(solution_text="Stay active and maintain a consistent daily routine."),
            CopingSolution(solution_text="Consult a mental health professional for SAD-specific therapies."),
            CopingSolution(solution_text="Engage in indoor hobbies or activities during poor weather."),
            CopingSolution(solution_text="Practice relaxation techniques to reduce stress and cabin fever."),
            CopingSolution(solution_text="Seek therapy for managing stress and coping with weather-induced stress."),
            CopingSolution(solution_text="Monitor your physical symptoms and seek medical advice as needed."),
            CopingSolution(solution_text="Stay active and maintain a healthy lifestyle regardless of the weather."),
            CopingSolution(solution_text="Consult healthcare professionals for addressing weather-induced physical issues."),
        ]

        db.session.bulk_save_objects(coping_solutions)
        db.session.commit()

# Link diagnoses and coping solutions
        print("Seeding diagnosis solutions...")
        diagnosis_solutions = [
            DiagnosisSolution(diagnosis_id=1, solution_id=1, solution_text="Stay informed about disaster preparedness and local resources."),
            DiagnosisSolution(diagnosis_id=1, solution_id=2, solution_text="Practice eco-friendly habits to reduce personal environmental impact."),
            DiagnosisSolution(diagnosis_id=1, solution_id=3, solution_text="Seek professional therapy to address anxiety and fears related to climate change."),
            DiagnosisSolution(diagnosis_id=2, solution_id=4, solution_text="Create an emergency plan for your family and home."),
            DiagnosisSolution(diagnosis_id=2, solution_id=5, solution_text="Stay active and maintain a consistent daily routine."),
            DiagnosisSolution(diagnosis_id=2, solution_id=6, solution_text="Consider professional therapy to address disaster-related anxiety."),
            DiagnosisSolution(diagnosis_id=3, solution_id=7, solution_text="Monitor weather forecasts and plan activities accordingly."),
            DiagnosisSolution(diagnosis_id=3, solution_id=8, solution_text="Engage in mood-boosting activities on gloomy days."),
            DiagnosisSolution(diagnosis_id=3, solution_id=9, solution_text="Consider therapy to manage mood swings influenced by the weather."),
            DiagnosisSolution(diagnosis_id=4, solution_id=10, solution_text="Use light therapy to mitigate the effects of reduced daylight."),
            DiagnosisSolution(diagnosis_id=4, solution_id=11, solution_text="Stay active and maintain a consistent daily routine."),
            DiagnosisSolution(diagnosis_id=4, solution_id=12, solution_text="Consult a mental health professional for SAD-specific therapies."),
            DiagnosisSolution(diagnosis_id=5, solution_id=13, solution_text="Engage in indoor hobbies or activities during poor weather."),
            DiagnosisSolution(diagnosis_id=5, solution_id=14, solution_text="Practice relaxation techniques to reduce stress and cabin fever."),
            DiagnosisSolution(diagnosis_id=5, solution_id=15, solution_text="Seek therapy for managing stress and coping with weather-induced stress."),
            DiagnosisSolution(diagnosis_id=6, solution_id=16, solution_text="Monitor your physical symptoms and seek medical advice as needed."),
            DiagnosisSolution(diagnosis_id=6, solution_id=17, solution_text="Stay active and maintain a healthy lifestyle regardless of the weather."),
            DiagnosisSolution(diagnosis_id=6, solution_id=18, solution_text="Consult healthcare professionals for addressing weather-induced physical issues."),
        ]

        db.session.bulk_save_objects(diagnosis_solutions)
        db.session.commit()

        print("Data seeded successfully.")

    if __name__ == '__main__':
        seed_data()


#in Ipython: 
# In [2]: %run seed.py
# In [3]: seed_data()


#___________DIRECTLY INTO POSTGRESSQL

# INSERT INTO groups (group_name, description) VALUES
# ('Climate Change Anxiety', 'Group for climate change-related discussions.'),
# ('Major Disaster/Severe Weather Anxiety', 'Group for extreme weather and disaster discussions.'),
# ('Weather makes me moody', 'Group for discussing mood and weather correlations.'),
# ('SAD', 'Group for Seasonal Affective Disorder (SAD) support.'),
# ('General Weather Stress/ Cabin Fever', 'Group for general weather-related stress discussions.'),
# ('Weather & Physical Health', 'Weather & Physical Health');


# INSERT INTO coping_solutions (solution_id, solution_text) VALUES
# (1, 'Stay informed about climate issues and actions you can take.'),
# (2, 'Practice eco-friendly habits to reduce personal environmental impact.'),
# (3, 'Seek professional therapy to address anxiety and fears related to climate change.'),
# (4, 'Create an emergency plan for your family and home.'),
# (5, 'Stay informed about disaster preparedness and local resources.'),
# (6, 'Consider professional therapy to address disaster-related anxiety.'),
# (7, 'Monitor weather forecasts and plan activities accordingly.'),
# (8, 'Engage in mood-boosting activities on gloomy days.'),
# (9, 'Consider therapy to manage mood swings influenced by the weather.'),
# (10, 'Use light therapy to mitigate the effects of reduced daylight.'),
# (11, 'Stay active and maintain a consistent daily routine.'),
# (12, 'Consult a mental health professional for SAD-specific therapies.'),
# (13, 'Engage in indoor hobbies or activities during poor weather.'),
# (14, 'Practice relaxation techniques to reduce stress and cabin fever.'),
# (15, 'Seek therapy for managing stress and coping with weather-induced stress.'),
# (16, 'Monitor your physical symptoms and seek medical advice as needed.'),
# (17, 'Stay active and maintain a healthy lifestyle regardless of the weather.'),
# (18, 'Consult healthcare professionals for addressing weather-induced physical issues');


# INSERT INTO diagnosis (issue_id, issue_name) VALUES
# (1, 'Climate Change or Environmental Anxiety'),
# (2, 'Major Disaster or Severe Weather Anxiety'),
# (3, 'Weather-Induced Mood Swings (Moody)'),
# (4, 'Seasonal Affective Disorder (SAD)'),
# (5, 'General Weather Stress or Cabin Fever'),
# (6, 'Weather-Induced Physical Issues');



# INSERT INTO diagnosis_solutions (id, diagnosis_id, solution_id) VALUES
# (1, 1, 1),
# (2, 1, 2),
# (3, 1, 3),
# (7, 2, 4),
# (8, 2, 5),
# (9, 2, 6),
# (13, 3, 7),
# (14, 3, 8),
# (15, 3, 9),
# (19, 4, 10),
# (20, 4, 11),
# (21, 4, 12),
# (25, 5, 13),
# (26, 5, 14),
# (27, 5, 15),
# (31, 6, 16),
# (32, 6, 17),
# (33, 6, 18);

 

#  then: -- 
# Update solution_text in diagnosis_solutions table based on coping_solutions

#  UPDATE diagnosis_solutions AS ds
#  SET solution_text = cs.solution_text
#  FROM coping_solutions AS cs
#  WHERE ds.solution_id = cs.solution_id;

# def update_diagnosis_solution_text():
#     # Update solution_text in diagnosis_solutions based on coping_solutions
#     db.session.execute(
#         '''
#         UPDATE diagnosis_solutions AS ds
#         SET solution_text = cs.solution_text
#         FROM coping_solutions AS cs
#         WHERE ds.solution_id = cs.solution_id;
#         '''
#     )
#     db.session.commit()