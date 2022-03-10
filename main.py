from datetime import datetime

from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bgcegy3yg2d3ue2uwccuby2ubwcchjsbgvcwcuwbc2whbuwb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bd.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    login = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Cabinet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(48))


class CleaningCabinet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number_cabinet = db.Column(db.String(48))
    date = db.Column(db.DateTime, default=datetime.utcnow)


db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if len(request.form.get('password')) < 4:
            flash('Please enter more(>4) password symbols', category='error')
        else:
            flash('Your user created!', category='success')

    name_user = 'John Johnovich'
    all_users = ['Charly', 'Matt', 'Richard', 'Kany']
    return render_template('index.html', user=name_user, all_users=all_users)


@app.route('/register')
def register():
    return render_template('register.html')


@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'), 404


if __name__ == '__main__':
    app.run()
