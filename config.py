import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KET') or 'hard to guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = 'True'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DETABASE_URI') or \
	'mysql://root:zhanglei@localhost/flask_db'

    @staticmethod
    def init__app(app):
        pass
