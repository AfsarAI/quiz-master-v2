from flask import Flask
from config import LocalDevelopmentConfig
from models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from flask_cors import CORS


app = None
def create_app():
    app = Flask(__name__, template_folder='frontend', static_folder='frontend', static_url_path='/static')

    app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    userdatastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, userdatastore, register_blueprint=False)
    app.app_context().push()

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

    from resources import api
    api.init_app(app)

    return app

app = create_app()


import initial_data
import routes

#for try!
if __name__ == '__main__':
    app.run()