from flask import current_app as app
from flask import jsonify, request
from flask_restful import Resource, marshal_with
from flask_security import auth_required
from models import Chapter, Qualification, Question, Quiz, RecentActivity, Subject, User, Score, UserQuizzes
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, User, Score
from .fields_definitions import activity_fields, qual_fields, score_fields, subjects_fields, user_fields, quizzes_fields, chapters_fields
from .user_api import add_recent_activity
cache = app.cache

class AdminStatsResource(Resource):
    @auth_required('token')
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
    @auth_required('token')
    @marshal_with(activity_fields)
    def get(self):
        one_week_ago = datetime.now() - timedelta(days=7)
        activities = RecentActivity.query.filter(RecentActivity.timestamp >= one_week_ago).order_by(RecentActivity.timestamp.desc()).limit(10).all()
        return activities


# Top Scorers api
class TopScorersResource(Resource):
    @auth_required('token')
    @marshal_with(score_fields)
    def get(self):
        top_scorers = db.session.query(Score).order_by(Score.score.desc()).limit(5).all()
        
        # Agar 5 se kam hain to sabhi return karo
        if len(top_scorers) < 5:
            return db.session.query(Score).order_by(Score.score.desc()).all()
        
        return top_scorers


    
# User api
class AllUsersResource(Resource):
    @cache.cached(timeout=300, key_prefix='users_data')
    @auth_required('token')
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

class UserStatusResource(Resource):
    @auth_required('token')
    def put(self, user_id):
        try:
            # Get the user by ID
            user = User.query.get(user_id)
            
            if not user:
                return {"message": "User not found"}, 404
                
            # Get the active status from request body
            data = request.get_json()
            active_status = data.get('active')
            
            if active_status is None:
                return {"message": "Active status is required"}, 400
                
            # Update user active status
            user.active = active_status
            db.session.commit()

            add_recent_activity(0, f"{user.fullname} {'Unblocked' if active_status else 'Blocked'} by Admin")
            
            cache.delete('users_data')
            cache.delete('userid_data')
            # Return updated user data
            return {
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
                "active": user.active,
                "message": f"User {'activated' if active_status else 'deactivated'} successfully"
            }, 200
            
        except Exception as e:
            db.session.rollback()
            return {"message": f"Error updating user status: {str(e)}"}, 500
        

class UserEngagementResource(Resource):
    @auth_required('token')
    def get(self):
        try:
            # Set time range (e.g., last 30 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)

            # Generate date labels
            date_labels = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(31)]

            # Score Distribution Logic
            score_ranges = ['0-20', '21-40', '41-60', '61-80', '81-100']
            score_counts = [
                Score.query.filter(Score.score.between(i, i+20)).count()
                for i in range(0, 100, 20)
            ]

            # Quiz Participation Logic
            quiz_participation = [
                db.session.query(User.id).join(Score).group_by(User.id).having(db.func.count(Score.id).between(r[0], r[1])).count()
                for r in [(1, 5), (6, 10), (11, 20), (21, 10000)]
            ]

            # Return response
            return jsonify({
                'labels': date_labels,
                'scoreRanges': score_ranges,
                'scoreCounts': score_counts,
                'quizParticipation': quiz_participation
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500


# ------------------------------------------------------------------------------------------ #

# Qualification api class for admin
class AllQualificationsResource(Resource):
    @auth_required('token')
    @marshal_with(qual_fields)
    def get(self):
        classes = Qualification.query.all()
        return classes
    
class AddQualificationResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        new_qual = Qualification(name=data['name'], description=data.get('description', ''))
        db.session.add(new_qual)
        db.session.commit()

        add_recent_activity(0, f"One Qualification Added by Admin")
        return {'message': 'Qualification added successfully!'}, 201
    
class UpdateQualificationResource(Resource):
    @auth_required('token')
    def put(self, qual_id):
        data = request.get_json()
        qualification = Qualification.query.get_or_404(qual_id)
        
        # Update qualification details
        qualification.name = data['name']
        qualification.description = data.get('description', '')
        
        db.session.commit()

        add_recent_activity(0, f"One Qualification Edited by Admin")
        return {'message': 'Qualification updated successfully!'}, 200
    
class DeleteQualificationResource(Resource):
    @auth_required('token')
    def delete(self, qual_id):
        qualification = Qualification.query.get_or_404(qual_id)
        
        # Find all subjects related to the qualification
        subjects = Subject.query.filter_by(qualification_id=qual_id).all()
        
        for subject in subjects:
            # Find all chapters related to the subject
            chapters = Chapter.query.filter_by(subject_id=subject.id).all()
            
            for chapter in chapters:
                # Find and delete all quizzes related to the chapter
                quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
                
                for quiz in quizzes:
                    # Delete associated scores
                    Score.query.filter_by(quiz_id=quiz.id).delete()
                    
                    # Delete associated questions
                    Question.query.filter_by(quiz_id=quiz.id).delete()
                    
                    # Delete UserQuizzes associations
                    UserQuizzes.query.filter_by(quiz_id=quiz.id).delete()
                    
                    # Delete the quiz
                    db.session.delete(quiz)
                
                # Delete the chapter
                db.session.delete(chapter)
            
            # Delete any remaining subject-specific quizzes
            quizzes = Quiz.query.filter_by(subject_id=subject.id).all()
            for quiz in quizzes:
                Score.query.filter_by(quiz_id=quiz.id).delete()
                Question.query.filter_by(quiz_id=quiz.id).delete()
                UserQuizzes.query.filter_by(quiz_id=quiz.id).delete()
                db.session.delete(quiz)
            
            # Delete the subject
            db.session.delete(subject)
        
        # Finally, delete the qualification
        db.session.delete(qualification)
        db.session.commit()
        
        add_recent_activity(0, f"One Qualification deleted by Admin")
        return {'message': 'Qualification and associated data deleted successfully!'}, 200

    


# Subject api class for admin
class AllSubjectsResource(Resource):
    @auth_required('token')
    @marshal_with(subjects_fields)
    def get(self):
        subjects = Subject.query.all()
        return subjects
    
class AddSubjectResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        print(data)
        new_subject = Subject(name=data['name'], description=data.get('description', ''), qualification_id=data['qualId'])
        db.session.add(new_subject)
        db.session.commit()

        add_recent_activity(0, f"One Subject added by Admin")
        return {'message': 'Subject added successfully!'}, 201

class UpdateSubjectResource(Resource):
    @auth_required('token')
    def put(self, subject_id):
        data = request.get_json()
        subject = Subject.query.get_or_404(subject_id)
        
        # Update subject details
        subject.name = data['name']
        subject.description = data.get('description', '')
        subject.qualification_id = data['qualId']
        
        db.session.commit()

        add_recent_activity(0, f"One Subject edited by Admin")
        return {'message': 'Subject updated successfully!'}, 200
    
class DeleteSubjectResource(Resource):
    @auth_required('token')
    def delete(self, subject_id):
        subject = Subject.query.get_or_404(subject_id)
        
        # Find all chapters related to the subject
        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        
        for chapter in chapters:
            # Find and delete all quizzes related to the chapter
            quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
            
            for quiz in quizzes:
                # Delete associated scores
                Score.query.filter_by(quiz_id=quiz.id).delete()
                
                # Delete associated questions
                Question.query.filter_by(quiz_id=quiz.id).delete()
                
                # Delete UserQuizzes associations
                UserQuizzes.query.filter_by(quiz_id=quiz.id).delete()
                
                # Delete the quiz
                db.session.delete(quiz)
            
            # Delete the chapter
            db.session.delete(chapter)
        
        # Delete any remaining subject-specific quizzes
        quizzes = Quiz.query.filter_by(subject_id=subject_id).all()
        for quiz in quizzes:
            Score.query.filter_by(quiz_id=quiz.id).delete()
            Question.query.filter_by(quiz_id=quiz.id).delete()
            UserQuizzes.query.filter_by(quiz_id=quiz.id).delete()
            db.session.delete(quiz)
        
        # Finally, delete the subject
        db.session.delete(subject)
        db.session.commit()
        
        add_recent_activity(0, f"One Subject deleted by Admin")
        return {'message': 'Subject and associated data deleted successfully!'}, 200


# Chapter api class for admin
class AllChaptersResource(Resource):
    @auth_required('token')
    @marshal_with(chapters_fields)
    def get(self):
        chapters = Chapter.query.all()
        return chapters

class AddChapterResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        new_chapter = Chapter(name=data['name'], description=data.get('description', ''), subject_id=data['subjectId'])
        db.session.add(new_chapter)
        db.session.commit()

        add_recent_activity(0, f"One Chapter added by Admin")
        return {'message': 'Chapter added successfully!'}, 201

class UpdateChapterResource(Resource):
    @auth_required('token')
    def put(self, chapter_id):
        data = request.get_json()
        chapter = Chapter.query.get_or_404(chapter_id)
        
        # Update chapter details
        chapter.name = data['name']
        chapter.description = data.get('description', '')
        chapter.subject_id = data['subjectId']
        
        db.session.commit()

        add_recent_activity(0, f"One Chapter edited by Admin")
        return {'message': 'Chapter updated successfully!'}, 200
    
class DeleteChapterResource(Resource):
    @auth_required('token')
    def delete(self, chapter_id):
        chapter = Chapter.query.get_or_404(chapter_id)
        
        # Find all quizzes related to the chapter
        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        
        for quiz in quizzes:
            # Delete associated scores
            Score.query.filter_by(quiz_id=quiz.id).delete()
            
            # Delete associated questions
            Question.query.filter_by(quiz_id=quiz.id).delete()
            
            # Delete UserQuizzes associations
            UserQuizzes.query.filter_by(quiz_id=quiz.id).delete()
            
            # Delete the quiz
            db.session.delete(quiz)
        
        # Then delete the chapter
        db.session.delete(chapter)
        db.session.commit()
        
        add_recent_activity(0, f"One Chapter deleted by Admin")
        return {'message': 'Chapter and associated data deleted successfully!'}, 200



# Quiz api class for admin
class AdminAllQuizzesResource(Resource):
    @cache.cached(timeout=60, key_prefix='quiz_data')
    @auth_required('token')
    @marshal_with(quizzes_fields)
    def get(self):
        quizzes = Quiz.query.all()
        return quizzes
    
class AddQuizResource(Resource):
    @auth_required('token')
    def post(self):
        data = request.get_json()
        print(data)
        
        # Pehle Quiz create karo
        new_quiz = Quiz(
                        title=data['title'],
                        quiz_type=data['quizType'],
                        qualification_id=data['qualificationId'],
                        subject_id=data['subjectId'],
                        chapter_id=data['chapterId'],
                        duration=data['duration']
                    )

        db.session.add(new_quiz)
        db.session.flush()  # Taake id mil sake bina commit kiye

        # Agar questions bhi aaye hain, toh unko bhi save karo
        questions = data.get("questions", [])
        print(questions)
        for q in questions:
            print(q)
            new_question = Question(
                quiz_id=new_quiz.id,
                question_text=q['text'],
                option1=q['options'][0]['text'],  # ✅ Fix: dictionary ke andar se value lo
                option2=q['options'][1]['text'],
                option3=q['options'][2]['text'],
                option4=q['options'][3]['text'],
                correct_option=q['correctAnswer'] + 1  # Convert from 0-based to 1-based indexing
            )
            db.session.add(new_question)

        db.session.commit()  # Sab data ek saath save hoga

        add_recent_activity(0, f"A new quiz added by admin")
        cache.delete('quiz_data')
        cache.delete('userquiz_data')
        return {"message": "Quiz and questions created successfully!", "quiz_id": new_quiz.id}, 201


# Add this new API endpoint to your resources file
class QuizDetailResource(Resource):
    @auth_required('token')
    @marshal_with(quizzes_fields)
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"error": "Quiz not found"}, 404
        return quiz

# Also update the edit functionality
class EditQuizResource(Resource):
    @auth_required('token')
    def put(self, quiz_id):
        data = request.get_json()
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Update quiz details
        quiz.title = data['title']
        quiz.quiz_type = data['quizType']
        quiz.qualification_id = data.get('qualificationId')
        quiz.subject_id = data.get('subjectId')
        quiz.chapter_id = data.get('chapterId')
        quiz.duration = data['duration']
        
        # Delete existing questions
        Question.query.filter_by(quiz_id=quiz_id).delete()
        
        # Add updated questions
        for q in data.get('questions', []):
            new_question = Question(
                quiz_id=quiz_id,
                question_text=q['text'],
                option1=q['options'][0]['text'],
                option2=q['options'][1]['text'],
                option3=q['options'][2]['text'],
                option4=q['options'][3]['text'],
                correct_option=q['correctAnswer'] + 1  # Keep this conversion consistent
            )
            db.session.add(new_question)
            
        db.session.commit()

        add_recent_activity(0, f"One quiz edited by admin")
        cache.delete('quiz_data')
        cache.delete('userquiz_data')
        return {"message": "Quiz updated successfully", "quiz_id": quiz_id}, 200


class DeleteQuizResource(Resource):
    @auth_required('token')
    def delete(self, quiz_id):
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Delete associated scores
        Score.query.filter_by(quiz_id=quiz_id).delete()

        # Delete associated questions
        Question.query.filter_by(quiz_id=quiz_id).delete()
        
        # Delete UserQuizzes associations
        UserQuizzes.query.filter_by(quiz_id=quiz_id).delete()

        # Then delete the quiz
        db.session.delete(quiz)
        db.session.commit()
        
        add_recent_activity(0, f"One quiz deleted by admin")
        cache.delete('quiz_data')
        cache.delete('userquiz_data')
        return {"message": "Quiz and associated data deleted successfully"}, 200