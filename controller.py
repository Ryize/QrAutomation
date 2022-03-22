from datetime import datetime

from flask import render_template, request, flash, make_response, url_for, redirect, session

from app import app, db
from models import User, Cabinet, ScheduleCleaning
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user


@app.before_request
def before_request():
    login()


@app.route('/', methods=['POST', 'GET'])
@app.route('/schedules', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/new_schedule', methods=['POST', 'GET'])
@login_required
def new_schedule():
    if request.method == 'POST':
        cabinet_id = request.form.get('cabinet')
        created_on = datetime.strptime(request.form.get('created_date'), "%Y-%m-%dT%H:%M")
        user_id = session['_user_id']
        schedule = ScheduleCleaning(cabinet_id=cabinet_id, user_id=user_id, created_on=created_on)
        db.session.add(schedule)
        db.session.commit()
    cabinets = Cabinet.query.all()
    return render_template('new_schedule.html', cabinets=cabinets)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'))
        try:
            user = User.register(username=username, surname=surname, patronymic=patronymic, email=email,
                                 password=password)
            login_user(user)
        except ValueError:
            flash('Ошибка регистрации!', category='error')

    return render_template('register.html', all_user=User.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Ошибка авторизации!', category='error')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login'))

    return response


@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'), 404