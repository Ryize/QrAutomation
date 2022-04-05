from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_migrate import Migrate

from config import DevelopmentConfig, ProductionConfig

app = Flask(__name__)

SITE_URL = '127.0.0.1:5000'
PRODUCTION = False

if PRODUCTION:
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate_bd = Migrate(app, db)

if __name__ == '__main__':
    from controller import app
    from logger import get_logger_handler

    app.logger.addHandler(get_logger_handler())
    app.run()
