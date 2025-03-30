import csv
from datetime import datetime, timedelta
from celery import shared_task
from sqlalchemy import func
from mail import send_email_template
from models import UserQuizzes, db, Score, Quiz, User
import requests

@shared_task(name="csv_file", ignore_results=False)
def create_csv_file(user_id):
    Scores = Score.query.filter_by(user_id=user_id).all()
    csvfilename = f"quiz_scores_{user_id}.csv"
    with open(f'csv/{csvfilename}', 'w', newline = "") as csvfile:

        sr_no = 1
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['Sr No.', 'Quiz ID', 'Quiz Name', 'Quiz Type', 'Subject Name', 'Chapter Name', 'Score', 'Time Taken', 'Attempt Date'])

        for score in Scores:
            quiz = Quiz.query.get(score.quiz_id)
            if not quiz:
                print(f"Error: Quiz with ID {score.quiz_id} not found.")
                continue

            csvwriter.writerow([
                sr_no,
                score.quiz_id,
                quiz.title,
                quiz.quiz_type,
                quiz.subject.name if quiz.subject else "N/A",
                quiz.chapter.name if quiz.chapter else "N/A",
                score.score,
                score.time_taken,
                score.attempt_date
            ])

            sr_no += 1

    return csvfilename


@shared_task(name="monthly_report", ignore_results=False)
def send_monthly_report():
    users = User.query.all()
    month = (datetime.now() - timedelta(days=1)).strftime('%B %Y')
    
    for user in users:
        # Get User Quiz Data
        quizzes = db.session.query(Quiz, Score).join(Score).filter(
            Score.user_id == user.id,
            Score.attempt_date >= datetime.now().replace(day=1) - timedelta(days=30)
        ).all()

        if not quizzes:
            continue

        # Prepare Quiz Data
        quiz_data = []
        for quiz, score in quizzes:
            avg_score = db.session.query(func.avg(Score.score)).filter(Score.quiz_id == quiz.id).scalar() or 0
            rank = db.session.query(func.count()).filter(Score.quiz_id == quiz.id, Score.score > score.score).scalar() + 1

            quiz_data.append({
                'title': quiz.title,
                'date_attempted': score.attempt_date.strftime('%Y-%m-%d'),
                'score': score.score,
                'average_score': round(avg_score, 2),
                'rank': rank
            })

        # Render HTML Email
        context = {'user_name': user.fullname, 'month': month, 'quizzes': quiz_data}

        # Send Email
        subject = f"Monthly Report - {month}"
        send_email_template(user.email, subject, 'templates/monthly_report.html', context, 'html')

    return "Monthly Reports Sent!"



WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAAAPn0TVg0/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Uzu7JnBKcZ6t9sI917kEGKW8PH5gmdGMdkvwISOJXdE"

@shared_task(name="daily_reminder", ignore_results=False)
def send_daily_reminder():
    # Find users who haven't attempted any quiz in the last 7 days (excluding admin with ID 1)
    last_week = datetime.now() - timedelta(days=7)
    inactive_users = User.query.filter(
        User.id != 1,  # Exclude Admin (assuming Admin has user_id = 1)
        ~User.id.in_(
            UserQuizzes.query
            .filter(UserQuizzes.attempt_date >= last_week)
            .with_entities(UserQuizzes.user_id)
        )
    ).all()

    # Find top 5 recent quizzes created in the last week
    recent_quizzes = Quiz.query.filter(Quiz.date_created >= last_week).limit(5).all()

    # Send message using Google Chat Webhook
    for user in inactive_users:
        # Construct user-specific URL
        quiz_links = [
            f"- *{quiz.title}*\nLink: http://localhost:8080/quiz-master/user/{user.id}/dashboard/quiz/{quiz.id}/interface\n"
            for quiz in recent_quizzes
        ]

        # Message content
        quiz_list_text = "\n".join(quiz_links)
        quiz_url = f"http://localhost:8080/quiz-master/user/{user.id}/dashboard/quiz"
        message_data = {
            "text": f"*Hello {user.fullname},*\n\nWe noticed you haven't taken any quizzes recently. "
                    f"Here are some new quizzes you might be interested in:\n\n"
                    f"{quiz_list_text}\n\n"
                    f"To see all available quizzes, (click here on link given below)\nLink: {quiz_url}\n\n"
                    f"Best regards,\nQuizMaster Team"
        }

        # Send the request
        response = requests.post(WEBHOOK_URL, json=message_data)
        if response.status_code == 200:
            return "Message sent to user via google chat"
        else:
            return "Failed to send reminder to user!"
    return "Daily reminders sent!"