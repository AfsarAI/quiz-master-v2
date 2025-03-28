import csv
from datetime import datetime, timedelta
import os
from celery import shared_task
from jinja2 import Template
from sqlalchemy import func
from mail import send_email_template
from models import db, Score, Quiz, User

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


# # second task
# def render_html_template(template_name, context):
#     template_path = os.path.join('templates', template_name)
#     with open(template_path, 'r') as file:
#         template = Template(file.read())
#         return template.render(context)

@shared_task(name="monthly_report", ignore_results=False)
def monthly_report():
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
        # html_content = render_html_template('monthly_report.html', context)

        # Send Email
        subject = f"Monthly Report - {month}"
        send_email_template(user.email, subject, 'templates/monthly_report.html', context, 'html')

    return "Monthly Reports Sent!"