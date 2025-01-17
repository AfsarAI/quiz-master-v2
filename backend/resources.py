from datetime import datetime
from flask import request, current_app as app
from flask_restful import Api, Resource, fields, marshal, marshal_with
from flask_security import auth_required, verify_password, hash_password
from models import db, Qualification, Subject, User
from sqlalchemy.exc import IntegrityError
from flask_security.utils import hash_password, verify_password
from flask_security import SQLAlchemyUserDatastore


api = Api(prefix='/api')

userdatastore: SQLAlchemyUserDatastore = app.security.datastore

subjects_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "qualification_id": fields.Integer
}

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "password": fields.String,
    "fullname": fields.String,
    "dob": fields.String,
    "qualification_id": fields.Integer,
    "profile_url": fields.String,
    "address": fields.String,
    "phone": fields.String,
    "roles": fields.List(fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
        "description": fields.String
    })),
    "subjects": fields.List(fields.Nested(subjects_fields)),
    "quizzes": fields.List(fields.String),
    "scores": fields.List(fields.String),
}


qual_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "subjects": fields.List(fields.String),
    "users": fields.List(fields.String)
}

class UserResource(Resource):
    @marshal_with(user_fields)
    @auth_required('token')
    def get(self):
        users = User.query.all()
        return users
    


# Assuming user_datastore is defined in your app.py
class UserRegisterResource(Resource):
    def post(self):
        data = request.get_json()
        
        # Extract data from the request
        email = data.get('email')
        password = data.get('password')
        fullname = data.get('fullname')
        dob = data.get('dob')
        gender = data.get('gender')
        qualification_id = data.get('qualification_id')
        subject_ids = data.get('subjects', [])  # List of subject IDs from frontend
        profile_url = data.get('profilePicUrl')
        address = data.get('address')
        phone = data.get('phone')

        # Basic validations
        if not email or not password or not fullname or not dob or not qualification_id:
            return {"message": "Missing required fields"}, 400

        # Check if the qualification exists
        qualification = Qualification.query.get(qualification_id)
        if not qualification:
            return {"message": "Qualification not found"}, 404

        # Check if the user already exists
        existing_user = userdatastore.find_user(email=email)
        if existing_user:
            return {"message": "User already registered. Please login."}, 400

        # Fetch Subject objects from IDs
        subjects = Subject.query.filter(Subject.id.in_(subject_ids)).all()
        if len(subjects) != len(subject_ids):
            return {"message": "Some subjects not found. Please check the IDs."}, 400

        # Create the user using Flask-Security
        try:
            dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            
            # Create the user
            new_user = userdatastore.create_user(
                email=email,
                password=hash_password(password),
                fullname=fullname,
                dob=dob,
                gender=gender,
                qualification_id=qualification_id,
                profile_url=profile_url,
                address=address,
                phone=phone,
                subjects=subjects  # Attach the subject objects here
            )

            # Assign the default role
            default_role = userdatastore.find_role('user')
            if default_role:
                userdatastore.add_role_to_user(new_user, default_role)

            # Commit the transaction
            db.session.commit()

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

        # Authenticate the user
        user = userdatastore.find_user(email=email)
        
        if not user:
            return {"message": "User not found"}, 404

        if not verify_password(password, user.password):
            return {"message": "Invalid password"}, 400

        # Generate the JWT token
        # token = userdatastore.create_token(user)
        token = user.get_auth_token()
         # Serialize user using user_fields
        serialized_user = marshal(user, user_fields)
        # Add the token to the response
        serialized_user["token"] = token
        return serialized_user, 200
    
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



class SubjectResource(Resource):

    @marshal_with(subjects_fields)
    @auth_required('token')
    def get(self):
        subjects = Subject.query.all()
        return subjects

    @auth_required('token')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        qualification_id = data.get('qualification_id')

        if not name:
            return {"message": "Subject name is required"}, 400

        # Check if the subject already exists
        existing_subject = Subject.query.filter_by(name=name).first()
        if existing_subject:
            return {"message": f"Subject '{name}' already exists"}, 400

        # Check if the qualification exists
        qualification = Qualification.query.get(qualification_id)
        if not qualification:
            return {"message": "Qualification not found"}, 404

        # Create the subject
        subject = Subject(name=name, description=description, qualification=qualification)
        db.session.add(subject)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "An unexpected error occurred"}, 500

        return {"message": "Subject created successfully"}, 201




class QualificationSubjectResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        subjects = data.get('subjects', [])

        if not name:
            return {"message": "Qualification name is required"}, 400

        # Check if the qualification already exists
        existing_qualification = Qualification.query.filter_by(name=name).first()
        if existing_qualification:
            return {"message": f"Qualification '{name}' already exists"}, 400

        # Create the qualification
        qualification = Qualification(name=name, description=description)
        db.session.add(qualification)

        # Add subjects to the qualification
        for subject_data in subjects:
            subject_name = subject_data.get('name')
            subject_description = subject_data.get('description')

            if not subject_name:
                return {"message": "Subject name is required"}, 400

            # Check if the subject already exists within the same qualification
            existing_subject = Subject.query.filter_by(
                name=subject_name,
                qualification_id=qualification.id  # Scoped by qualification
            ).first()
            if existing_subject:
                return {
                    "message": f"Subject '{subject_name}' already exists in qualification '{name}'"
                }, 400

            # Add the subject
            subject = Subject(name=subject_name, description=subject_description, qualification=qualification)
            db.session.add(subject)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "An unexpected error occurred"}, 500

        return {"message": "Qualification and subjects created successfully"}, 201



api.add_resource(UserResource, '/users/data')
api.add_resource(UserRegisterResource, '/user/register', methods=['POST'])
api.add_resource(UserLoginResource, '/user/login', methods=['POST'])
api.add_resource(QualificationResource, '/qualifications')
api.add_resource(SubjectsWithQualificationResource, '/qualifications/<int:qualification_id>/subjects')
api.add_resource(SubjectResource, '/subjects')
api.add_resource(QualificationSubjectResource, '/create/qualification-subjects')