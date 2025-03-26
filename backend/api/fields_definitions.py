from flask_restful import fields

chapters_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "subject_id": fields.Integer
}

subjects_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "qualification_id": fields.Integer,
    "chapters": fields.List(fields.Nested(chapters_fields))
}


quizzes_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "quiz_type": fields.String,
    "subject_id": fields.Integer,
    "chapter_id": fields.Integer,
    "date_created": fields.DateTime,
    "duration": fields.Integer,
    "questions": fields.List(fields.String)
}


score_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "quiz_id": fields.Integer,
    "score": fields.Float,
    "attempt_date": fields.DateTime,
    "active": fields.Boolean
}

user_fields = {
    "id": fields.Integer,
    "email": fields.String,
    "password": fields.String,
    "fullname": fields.String,
    "dob": fields.String,
    "gender":fields.String,
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
    "quizzes": fields.List(fields.Nested(quizzes_fields)),
    "scores": fields.List(fields.Nested(score_fields)),
}


qual_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "subjects": fields.List(fields.String),
    "users": fields.List(fields.String)
}


activity_fields = {
            'id': fields.Integer,
            'user': fields.String,
            'action': fields.String,
            'timestamp': fields.DateTime
        }