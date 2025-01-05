class config():
    DEBUG = False
    SQLALCHEMY_TRACH_MODIFICATIONS = False

class LocalDevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quizmaster.db'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'somesalt'
    SECRET_KEY = 'supersecretkey'

    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'