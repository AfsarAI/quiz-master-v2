from flask import Flask
from config import LocalDevelopmentConfig
from models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS
from celery_init import celery_init_app
from celery.schedules import crontab
from flask_caching import Cache

app = None
def create_app():
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')

    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    cache = Cache(app)

    userdatastore = SQLAlchemyUserDatastore(db, User, Role)
    app.cache = cache
    app.security = Security(app, userdatastore, register_blueprint=False)
    app.app_context().push()

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    from api.setup_api import api
    api.init_app(app)

    return app

app = create_app()
celery = celery_init_app(app)
celery.autodiscover_tasks()

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily Reminder - Every 2 minutes
    sender.add_periodic_task(
        crontab(minute='*/2'),
        tasks.send_daily_reminder.s(),
    )

    # Monthly Report - Every 3 minutes (for testing purpose)
    sender.add_periodic_task(
        crontab(minute='*/3'),
        tasks.send_monthly_report.s(),
    )


import initial_data
import base_route as routes
import tasks

#for try!
if __name__ == '__main__':
    app.run()