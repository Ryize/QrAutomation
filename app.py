from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)


class Config:
    SECRET_KEY = 'bgcegy3yg2d3ue2uwccuby2ubwcchjsbgvcwcuwbc2whbuwb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


SITE_URL = '127.0.0.1:5000'

app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate_bd = Migrate(app, db)

if __name__ == '__main__':
    from controller import app

    app.run(debug=True)
