from flask import request, current_app as app
from flask_restful import Api, Resource, fields, marshal_with
from flask_security import auth_required
from models import db, Qualification, Subject
from sqlalchemy.exc import IntegrityError

api = Api(prefix='/api')

qual_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "subjects": fields.List(fields.String),
    "users": fields.List(fields.String)
}

class QualificationResource(Resource):
    @marshal_with(qual_fields)
    def get(self):
        qualifications = Qualification.query.all()
        return qualifications

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

api.add_resource(QualificationResource, '/qualifications')
api.add_resource(QualificationSubjectResource, '/create/qualification-subjects')