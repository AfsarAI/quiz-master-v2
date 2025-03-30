from flask import current_app as app
from flask_restful import Resource, marshal_with, marshal
from flask_security import auth_required, verify_password, hash_password
from flask import request, jsonify
from datetime import datetime
from models import Quiz, db, User, Subject, Qualification
from sqlalchemy.exc import IntegrityError
from flask_security.utils import hash_password, verify_password
from flask_security import SQLAlchemyUserDatastore
from .fields_definitions import user_fields, subjects_fields, qual_fields
from .user_api import add_recent_activity


userdatastore: SQLAlchemyUserDatastore = app.security.datastore



# Qualification & Subjects Api for Registration Page
class QualificationResource(Resource):
    @marshal_with(qual_fields)
    def get(self):
        qualifications = Qualification.query.all()
        return qualifications

class SubjectsWithQualificationResource(Resource):
    @marshal_with(subjects_fields)
    def get(self, qualification_id):
        subjects = Subject.query.filter_by(qualification_id=qualification_id).all()
        return subjects


# For Login & Register Api
class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')
        dob = data.get('dob')
        gender = data.get('gender')
        qualification_id = data.get('qualification_id')
        subject_ids = data.get('subjects', [])
        profile_url = data.get('profilePicUrl')
        address = data.get('address')
        phone = data.get('phone')

        if not email or not password or not fullname or not dob or not qualification_id:
            return {"message": "Missing required fields"}, 400

        qualification = Qualification.query.get(qualification_id)
        if not qualification:
            return {"message": "Qualification not found"}, 404

        existing_user = userdatastore.find_user(email=email)
        if existing_user:
            return {"message": "User already registered. Please login."}, 400

        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
        if len(subjects) != len(subject_ids):
            return {"message": "Some subjects not found. Please check the IDs."}, 400

        try:
            parsed_dob = datetime.strptime(dob, '%Y-%m-%d').date()
            new_user = userdatastore.create_user(
                email=email,
                password=hash_password(password),
                fullname=fullname,
                dob=parsed_dob,
                gender=gender,
                qualification_id=qualification_id,
                profile_url=profile_url,
                address=address,
                phone=phone,
                subjects=subjects
            )

            default_role = userdatastore.find_role('user')
            if default_role:
                userdatastore.add_role_to_user(new_user, default_role)

            db.session.commit()
            add_recent_activity(user_id=new_user.id, action=f"Now {new_user.fullname} registered on this website")           
        except Exception as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500

        return {"message": "User created successfully"}, 201

class UserLoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email:
            return {"message": "Email is required"}, 400
        if not password:
            return {"message": "Password is required"}, 400

        user = userdatastore.find_user(email=email)
        if not user:
            return {"message": "User not found"}, 404

        if not user.active:
            return {"message": "Your account is inactive"}, 403

        if not verify_password(password, user.password):
            return {"message": "Invalid password"}, 400

        token = user.get_auth_token()
        serialized_user = marshal(user, user_fields)
        serialized_user["token"] = token
        return serialized_user, 200

