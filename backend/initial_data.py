from flask import current_app as app
from models import db, User, Role, Qualification, Subject
from flask_security import SQLAlchemyUserDatastore, hash_password
from datetime import datetime

def create_initial_data():
    with app.app_context():
        # Initialize the database
        db.create_all()

        userdatastore: SQLAlchemyUserDatastore = app.security.datastore

        # Create roles with error handling
        try:
            admin_role = userdatastore.find_or_create_role(name='admin', description='Superuser')
            user_role = userdatastore.find_or_create_role(name='user', description='General user')
        except Exception as e:
            print(f"Error creating roles: {e}")

        # Create users with checks
        try:
            if not userdatastore.find_user(email='admin@study.iitm.ac.in'):
                admin_qualification = Qualification.query.filter_by(name="B.Tech").first()  # Assign a valid qualification
                userdatastore.create_user(
                    email='admin@study.iitm.ac.in',
                    password=hash_password('pass'),
                    fullname='Admin User',
                    dob=datetime.strptime('1980-01-01', '%Y-%m-%d'),
                    qualification_id=admin_qualification.id,  # Provide a valid qualification ID
                    roles=[admin_role]
                )
            else:
                print("Admin user already exists.")

            if not userdatastore.find_user(email='user01@study.iitm.ac.in'):
                user_qualification = Qualification.query.filter_by(name="M.Tech").first()  # Assign a valid qualification
                userdatastore.create_user(
                    email='user01@study.iitm.ac.in',
                    password=hash_password('pass'),
                    fullname='Test User',
                    dob=datetime.strptime('2000-01-01', '%Y-%m-%d'),
                    qualification_id=user_qualification.id,  # Provide a valid qualification ID
                    roles=[user_role]
                )
            else:
                print("Test user already exists.")
        except Exception as e:
            print(f"Error creating users: {e}")


        # Create qualifications with checks
        qualifications_data = [
            {"name": "B.Tech", "description": "Bachelor of Technology"},
            {"name": "M.Tech", "description": "Master of Technology"},
            {"name": "PhD", "description": "Doctor of Philosophy"},
        ]

        for qualification in qualifications_data:
            try:
                if not Qualification.query.filter_by(name=qualification['name']).first():
                    db.session.add(Qualification(name=qualification['name'], description=qualification['description']))
                else:
                    print(f"Qualification '{qualification['name']}' already exists.")
            except Exception as e:
                print(f"Error creating qualification '{qualification['name']}': {e}")

        db.session.commit()  # Commit qualifications to ensure subjects can reference them

        # Create subjects with checks
        subjects_data = [
            {"name": "Mathematics", "description": "Core subject for engineering.", "qualification_name": "B.Tech"},
            {"name": "Physics", "description": "Fundamental physical sciences.", "qualification_name": "B.Tech"},
            {"name": "Machine Learning", "description": "Advanced topic in AI.", "qualification_name": "M.Tech"},
            {"name": "Quantum Computing", "description": "Study of quantum algorithms.", "qualification_name": "PhD"},
        ]

        for subject in subjects_data:
            try:
                qualification = Qualification.query.filter_by(name=subject['qualification_name']).first()
                if qualification and not Subject.query.filter_by(name=subject['name']).first():
                    db.session.add(Subject(
                        name=subject['name'],
                        description=subject['description'],
                        qualification_id=qualification.id
                    ))
                else:
                    print(f"Subject '{subject['name']}' already exists or qualification not found.")
            except Exception as e:
                print(f"Error creating subject '{subject['name']}': {e}")

        # Final commit
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error committing changes to database: {e}")

# Call the function to seed data
create_initial_data()