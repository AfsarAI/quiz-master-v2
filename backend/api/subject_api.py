from flask_restful import Resource, marshal_with
from flask_security import auth_required
from flask import request
from sqlalchemy.exc import IntegrityError

from models import db, Subject, Qualification
from .fields_definitions import subjects_fields

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

        existing_subject = Subject.query.filter_by(name=name).first()
        if existing_subject:
            return {"message": f"Subject '{name}' already exists"}, 400

        qualification = Qualification.query.get(qualification_id)
        if not qualification:
            return {"message": "Qualification not found"}, 404

        subject = Subject(name=name, description=description, qualification=qualification)
        db.session.add(subject)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"error": "An unexpected error occurred"}, 500

        return {"message": "Subject created successfully"}, 201


class SubjectsWithQualificationResource(Resource):
    @marshal_with(subjects_fields)
    def get(self, qualification_id):
        subjects = Subject.query.filter_by(qualification_id=qualification_id).all()
        return subjects
