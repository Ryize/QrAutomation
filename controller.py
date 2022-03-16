from flask import render_template, request, flash, make_response, url_for, redirect

from main import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user


@app.before_request
def before_request():
    login()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if len(request.form.get('password')) > 3 and request.form.get('password') == '1234':
            res = make_response(render_template('index.html'))
            res.set_cookie('username', request.form.get('username'), max_age=60 * 60 * 24 * 31 * 12)
            res.set_cookie('username', request.form.get('password'), max_age=60 * 60 * 24 * 31 * 12)
            return res, 200
        else:
            flash('Please enter more(>4) password symbols', category='error')

    return render_template('index.html')


@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    return 'admin!'


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
            return render_template('login.html')
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
