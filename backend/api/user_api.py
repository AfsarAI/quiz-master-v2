from flask import current_app as app
from flask import request, send_from_directory
from flask_restful import Resource, marshal, marshal_with
from flask_security import auth_required
from tasks import create_csv_file
from models import Chapter, Quiz, RecentActivity, User, Score, UserSubjects
from datetime import datetime, timedelta
from celery.result import AsyncResult
from models import db, User, Score
from .fields_definitions import score_fields, subjects_fields, quizzes_fields, user_fields
cache = app.cache

# Add recent activity
def add_recent_activity(user_id, action):
    try:
        new_activity = RecentActivity(
            user_id=user_id,
            action=action,
            timestamp=datetime.now()
        )
        db.session.add(new_activity)
        db.session.commit()
        print("Recent activity added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding recent activity: {e}")


# for profile page
class UserByIDResource(Resource):
    @auth_required('token')
    @cache.cached(timeout=300, key_prefix='userid_data')
    @marshal_with(user_fields)
    def get(self, user_id):
        user = User.query.get(user_id)
        return user
    


#for home page
class UserStatsResource(Resource):
    @auth_required('token')
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
    @auth_required()
    @marshal_with(quizzes_fields)
    def get(self):
        quizzes = Quiz.query.filter(Quiz.date_created <= datetime.now()).limit(5).all()
        return quizzes, 200

class QuizScoresResource(Resource):
    @auth_required('token')
    def get(self, user_id):
        user_scores = Score.query.filter_by(user_id=user_id).order_by(Score.attempt_date.desc()).all()
        if not user_scores:
            return {"message": "No scores available"}, 404

        # Marshal karna sirf tab hoga jab data milega
        return marshal(user_scores, score_fields), 200

    

# For quiz page
class UserAllQuizzesResource(Resource):
    @auth_required('token')
    @cache.cached(timeout=300, key_prefix='userquiz_data')
    @marshal_with(quizzes_fields)
    def get(self, user_id):
        # Fetch user details
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        if not user.qualification_id:
            return {'message': 'User qualification not set'}, 404

        # Fetch user selected subjects using subquery
        user_subjects = db.session.query(UserSubjects.subject_id).filter_by(user_id=user_id).scalar_subquery()

        # Get quizzes using explicit select to avoid warnings
        quizzes = db.session.query(Quiz).filter(
            db.or_(
                db.and_(
                    Quiz.quiz_type == 'whole',
                    Quiz.qualification_id == user.qualification_id
                ),
                db.and_(
                    Quiz.quiz_type == 'subject',
                    Quiz.subject_id.in_(user_subjects)
                ),
                db.and_(
                    Quiz.quiz_type == 'chapter',
                    Quiz.chapter.has(
                        Chapter.subject_id.in_(user_subjects)
                    )
                )
            )
        ).all()
        
        if not quizzes:
            return {"message": "No quizzes available"}, 404
        
        # Calculate attempt count for each quiz
        for quiz in quizzes:
            quiz.attempt_count = Score.query.filter_by(user_id=user_id, quiz_id=quiz.id).count()

        return quizzes, 200



# For quiz portel page
class UserQuizResource(Resource):
    @auth_required('token')
    @marshal_with(quizzes_fields)
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return {"error": "Quiz not found"}, 404
        
        return quiz, 200

class SubmitQuizResource(Resource):
    @auth_required('token')
    def post(self, quiz_id):
        data = request.get_json()
        user_id = data.get('userId')
        user = User.query.get(user_id)

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
 
            # Add recent activity
            add_recent_activity(user_id, f"{user.fullname} Completed a quiz")
            cache.delete('userid_data')
            return {"message": "Quiz submitted successfully!"}, 200

        return {"error": "Invalid data provided"}, 400




# Backend things! (csv export)
class TaskCSVResource(Resource):
    @auth_required('token')
    def get(self, user_id):
        task = create_csv_file.delay(user_id)
        user = User.query.get(user_id)
        add_recent_activity(user_id, f"{user.fullname} Downloaded the details of the quizzes he was given")
        return {"task_id": task.id, "message": "CSV generation started"}, 200

    
class TaskStatusResource(Resource):
    def get(self, task_id):
        task = AsyncResult(task_id)
        
        if not task:
            return {"error": "Invalid Task ID"}, 404
        
        # Check task status
        if task.state == 'SUCCESS':
            csv_filename = task.result
            return send_from_directory('csv', csv_filename, as_attachment=True)
        elif task.state == 'FAILURE':
            return {"task_status": task.state, "error": str(task.info)}, 500
        elif task.state == 'PENDING':
            return {"task_status": task.state, "message": "Task is still in progress. Please check again later."}, 202
        else:
            return {"task_status": task.state}, 200
