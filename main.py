from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config:
    SECRET_KEY = 'bgcegy3yg2d3ue2uwccuby2ubwcchjsbgvcwcuwbc2whbuwb'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bd.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

db = SQLAlchemy(app)

if __name__ == '__main__':
    from controller import app

    app.run(debug=True)
