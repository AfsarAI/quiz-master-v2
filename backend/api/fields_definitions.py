from flask_restful import fields


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
