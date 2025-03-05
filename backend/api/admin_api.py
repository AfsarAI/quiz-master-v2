from flask import jsonify, request
from flask_restful import Resource, marshal_with
from models import Chapter, Qualification, Quiz, RecentActivity, Subject, User, Score
from datetime import datetime, timedelta
from sqlalchemy import func

from models import db, User, Score
from .fields_definitions import activity_fields, qual_fields, score_fields, subjects_fields



class AdminStatsResource(Resource):
    def get(self):
        total_users = User.query.count()
        active_quizzes = Score.query.filter_by(active=True).count()
        quizzes_taken = db.session.query(Score).count()
        avg_score = db.session.query(func.avg(Score.score)).scalar() or 0

        # Calculate previous week's stats
        one_week_ago = datetime.now() - timedelta(days=7)
        prev_total_users = User.query.filter(User.created_at < one_week_ago).count()
        prev_active_quizzes = db.session.query(Score).filter(Score.active == True, Score.attempt_date < one_week_ago).count()
        prev_quizzes_taken = db.session.query(Score).filter(Score.attempt_date < one_week_ago).count()
        prev_avg_score = db.session.query(func.avg(Score.score)).filter(Score.attempt_date < one_week_ago).scalar() or 0

        return jsonify({
            "stats": [
                {"title": "Total Users", "value": total_users, "previous": prev_total_users},
                {"title": "Active Quizzes", "value": active_quizzes, "previous": prev_active_quizzes},
                {"title": "Quizzes Taken", "value": quizzes_taken, "previous": prev_quizzes_taken},
                {"title": "Avg. Quiz Score", "value": f"{avg_score:.2f}%", "previous": f"{prev_avg_score:.2f}%"}
            ]
        })


        

class AllRecentActivityResource(Resource):
    @marshal_with(activity_fields)
    def get(self):
        one_week_ago = datetime.now() - timedelta(days=7)
        activities = RecentActivity.query.filter(RecentActivity.timestamp >= one_week_ago).order_by(RecentActivity.timestamp.desc()).limit(10).all()
        return activities

class RecentActivityResource(Resource):
    def post(self):
        data = request.json
        new_activity = RecentActivity(user=data['user'], action=data['action'])
        db.session.add(new_activity)
        db.session.commit()
        return jsonify({"message": "Activity logged successfully!"}), 201

class TopScorersResource(Resource):
    @marshal_with(score_fields)
    def get(self):
        top_scorers = db.session.query(Score).order_by(Score.score.desc()).limit(5).all()
        return top_scorers

class AllQualificationsResource(Resource):
    @marshal_with(qual_fields)
    def get(self):
        classes = Qualification.query.all()
        return classes
    
class AllSubjectsResource(Resource):
    @marshal_with(subjects_fields)
    def get(self):
        subjects = Subject.query.all()
        return subjects


# adding class, subject, chapter
class AddQualificationResource(Resource):
    def post(self):
        data = request.get_json()
        new_qual = Qualification(name=data['name'], description=data.get('description', ''))
        db.session.add(new_qual)
        db.session.commit()
        return {'message': 'Qualification added successfully!'}, 201
    
class AddSubjectResource(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        new_subject = Subject(name=data['name'], description=data.get('description', ''), qualification_id=data['qualId'])
        db.session.add(new_subject)
        db.session.commit()
        return {'message': 'Subject added successfully!'}, 201

class AddChapterResource(Resource):
    def post(self):
        data = request.get_json()
        new_chapter = Chapter(name=data['name'], description=data.get('description', ''), subject_id=data['subjectId'])
        db.session.add(new_chapter)
        db.session.commit()
        return {'message': 'Chapter added successfully!'}, 201


# All things!
class AllUsersResource(Resource):
    @marshal_with(qual_fields)
    def get(self):
        users = User.query.all()
        return users

class AllScoresResource(Resource):
    @marshal_with(score_fields)
    def get(self):
        scores = Score.query.all()
        return scores

class AllQuizzesResource(Resource):
    @marshal_with(score_fields)
    def get(self):
        quizzes = Quiz.query.all()
        return quizzes