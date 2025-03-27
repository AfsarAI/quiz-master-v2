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

questions_fields = {
    "id": fields.Integer,
    "question_text": fields.String,
    "options": fields.List(fields.String, attribute=lambda x: [x.option1, x.option2, x.option3, x.option4]),
    "correct_option": fields.String,
    "subject_id": fields.Integer,
    "chapter_id": fields.Integer,
    "quiz_id": fields.Integer
}

quizzes_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "quiz_type": fields.String,
    "subject_id": fields.Integer,
    "chapter_id": fields.Integer,
    "date_created": fields.String(attribute=lambda x: x.date_created.strftime('%Y-%m-%d %H:%M:%S')),
    "duration": fields.Integer,
    "questions": fields.List(fields.Nested(questions_fields)),
    "subject": fields.Nested(subjects_fields, allow_null=True),
    "chapter": fields.Nested(chapters_fields, allow_null=True)
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