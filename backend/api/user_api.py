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

        streak_message = f"{streak} day" if streak > 0 else "-1 day"

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
    @marshal_with(quizzes_fields)
    def get(self):
        quizzes = Quiz.query.filter(Quiz.date_created <= datetime.now()).limit(3).all()
        # data = [{"id": quiz.id, "title": quiz.title, "subject": quiz.quiz_type, "date": str(quiz.date_created)} for quiz in quizzes]
        return quizzes, 200

class UserSubjectsResource(Resource):
    # @auth_required()
    @marshal_with(subjects_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"error": "User not found"}, 404
        subjects = user.subjects
        return subjects, 200


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
    # @auth_required()
    @marshal_with(quizzes_fields)
    def get(self):
        quizzes = Quiz.query.all()
        # data = [{"id": quiz.id, "title": quiz.title, "subject": quiz.quiz_type, "duration": quiz.duration} for quiz in quizzes]
        return quizzes, 200
    

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


class SubmitQuizResource(Resource):
    def post(self, quiz_id):
        data = request.get_json()
        user_id = data.get('userId')

        if not user_id:
            return {"error": "User ID is required"}, 400

        # Check if quiz exists
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"error": "Quiz not found"}, 404

        # Check if it's a start request or a submit request
        if 'startTime' in data:
            # Start Quiz Logic
            start_time = data.get('startTime')

            # Check for an existing active attempt
            existing_attempt = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id, active=True).first()

            if existing_attempt:
                # Update existing attempt (Restart)
                existing_attempt.attempt_date = datetime.fromisoformat(start_time)
                existing_attempt.score = 0.0
                existing_attempt.time_taken = 0
                db.session.commit()
                return {"message": "Quiz restarted successfully!", "score_id": existing_attempt.id}, 200

            # Create new attempt
            new_score = Score(
                user_id=user_id,
                quiz_id=quiz_id,
                score=0.0,
                time_taken=0,
                attempt_date=datetime.fromisoformat(start_time),
                active=True
            )
            db.session.add(new_score)
            db.session.commit()
            return {"message": "Quiz started successfully!", "score_id": new_score.id}, 201

        elif 'score' in data:
            # Submit Quiz Logic
            score = data.get('score')
            time_taken = data.get('timeTaken')

            attempt = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id, active=True).first()
            if not attempt:
                return {"error": "No active attempt found to submit"}, 404

            # Update the score
            attempt.score = score
            attempt.time_taken = time_taken
            attempt.active = False
            db.session.commit()
            return {"message": "Quiz submitted successfully!"}, 200

        return {"error": "Invalid data provided"}, 400