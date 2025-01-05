from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    qualification_id = db.Column(db.Integer, db.ForeignKey('qualification.id'), nullable=False)
    profile_url = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String)
    phone = db.Column(db.String)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Relationships
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))
    subjects = db.relationship('Subject', secondary='user_subjects', backref=db.backref('users', lazy='dynamic'))
    quizzes = db.relationship('Quiz', secondary='user_quizzes', backref=db.backref('users', lazy='dynamic'))
    scores = db.relationship('Score', backref='user', lazy=True)


# Role Model
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

# UserRoles Association Table
class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))



# Qualification Model
class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Relationships
    subjects = db.relationship('Subject', backref='qualification', lazy=True)
    users = db.relationship('User', backref='qualification', lazy=True)


# Subject Model
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    qualification_id = db.Column(db.Integer, db.ForeignKey('qualification.id'), nullable=False)

    # Relationships
    chapters = db.relationship('Chapter', backref='subject', lazy=True)
    questions = db.relationship('Question', backref='subject', lazy=True)


# UserSubjects Association Table
class UserSubjects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'))

# Chapter Model
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    
    # Relationships
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)
    questions = db.relationship('Question', backref='chapter', lazy=True)


# Quiz Model
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    quiz_type = db.Column(db.String(50), nullable=False)  # 'whole', 'subject', or 'chapter'
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True)
    scores = db.relationship('Score', backref='quiz', lazy=True)


# UserQuizzes Association Table
class UserQuizzes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'))
    attempt_date = db.Column(db.DateTime, default=datetime.now)



# Question Model
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)  # Question belongs to a subject
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=True)  # Question belongs to a chapter
    question_text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.String(10), nullable=False)


# Score Model
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    attempt_date = db.Column(db.DateTime, default=datetime.now, nullable=False)