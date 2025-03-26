from flask import jsonify, request
from flask_restful import Resource, marshal_with
from flask_security import auth_required
from models import Chapter, Qualification, Question, Quiz, RecentActivity, Subject, User, Score
from datetime import datetime, timedelta
from sqlalchemy import func

from models import db, User, Score
from .fields_definitions import activity_fields, qual_fields, score_fields, subjects_fields, user_fields, quizzes_fields, chapters_fields


class UserStatsResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        
        if not user:
            return {"error": "User not found"}, 404

        total_quizzes = len(user.scores)
        average_score = (
            db.session.query(db.func.avg(Score.score))
            .filter(Score.user_id == user.id)
            .scalar() or 0
        )

        subjects_count = len(user.subjects)

        # Calculate the steady streak
        today = datetime.now().date()
        seven_days_ago = today - timedelta(days=7)
        recent_activities = (
            db.session.query(RecentActivity)
            .filter(RecentActivity.user_id == user.id, RecentActivity.timestamp >= seven_days_ago)
            .order_by(RecentActivity.timestamp.desc())
            .all()
        )

        streak = 0
        for i in range(7):
            day = today - timedelta(days=i)
            if any(activity.timestamp.date() == day for activity in recent_activities):
                streak += 1
            else:
                break

        streak_message = f"{streak} day streak" if streak > 0 else "1 day beyond"

        return {
            "user_stats_data": [
                {"title": "Quizzes Taken", "value": total_quizzes, "icon": "bi bi-journal-check"},
                {"title": "Average Score", "value": f"{average_score:.2f}%", "icon": "bi bi-graph-up"},
                {"title": "Steady Streak", "value": streak_message, "icon": "bi bi-fire"},
                {"title": "Subjects", "value": subjects_count, "icon": "bi bi-book"},
            ]
        }, 200


class UpcomingQuizzesResource(Resource):
    # @auth_required()
    def get(self):
        quizzes = Quiz.query.filter(Quiz.date_created >= datetime.now()).limit(3).all()
        data = [{"id": quiz.id, "title": quiz.title, "subject": quiz.quiz_type, "date": str(quiz.date_created)} for quiz in quizzes]
        return jsonify(data)

class UserSubjectsResource(Resource):
    # @auth_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        
        if not user:
            return {"error": "User not found"}, 404

        subjects = user.subjects
        data = [{"id": subject.id, "name": subject.name, "icon": "bi bi-book"} for subject in subjects]
        return data, 200


class QuizScoresResource(Resource):
    # @auth_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        
        if not user:
            return {"error": "User not found"}, 404

        scores = Score.query.filter_by(user_id=user.id).order_by(Score.attempt_date.desc()).limit(6).all()
        score_data = [score.score for score in scores]
        return score_data, 200

class UserAllQuizzesResource(Resource):
    def get(self):
        quizzes = Quiz.query.all()
        data = [{"id": quiz.id, "title": quiz.title, "subject": quiz.quiz_type, "duration": quiz.duration} for quiz in quizzes]
        return data, 200
    

class UserQuizResource(Resource):
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return {"error": "Quiz not found"}, 404

        questions = quiz.questions
        
        if not questions:
            return {"error": "No questions available for this quiz"}, 404
        
        data = {
            "quiz_id": quiz.id,
            "title": quiz.title,
            "quiz_type": quiz.quiz_type,
            "duration": quiz.duration,
            "date_created": quiz.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            "questions": [
                {
                    "id": question.id,
                    "question": question.question_text,
                    "options": [
                        question.option1,
                        question.option2,
                        question.option3,
                        question.option4
                    ],
                    "answer": question.correct_option,
                }
                for question in questions
            ]
        }
        
        return data, 200