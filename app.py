import flask_monitoringdashboard as dashboard
import smtplib

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager
from flask_migrate import Migrate

from flask_toastr import Toastr

from flask_maintenance import Maintenance

from flask_debugtoolbar import DebugToolbarExtension

from config import DevelopmentConfig, ProductionConfig, CustomConfig

app = Flask(__name__)

if CustomConfig.PRODUCTION:
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate_bd = Migrate(app, db)
toastr = Toastr(app)
dashboard.bind(app)
Maintenance(app)
DebugToolbarExtension(app)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(CustomConfig.MAIL_ADDRESS, CustomConfig.MAIL_PASSWORD)


if __name__ == '__main__':
    from controller import app
    from admin import app
    from logger import get_logger_handler

    app.logger.addHandler(get_logger_handler())
    app.run()
    server.quit()
