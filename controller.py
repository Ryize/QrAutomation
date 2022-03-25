from datetime import datetime

from flask import render_template, request, flash, url_for, redirect, session

from app import app, db
from models import User, Cabinet, ScheduleCleaning
from flask_login import login_required, logout_user, login_user


@app.route('/', methods=['POST', 'GET'])
@app.route('/schedules', methods=['POST', 'GET'])
def index():
    search = request.args.get('query')
    schedules = ScheduleCleaning.query.order_by(ScheduleCleaning.created_on.desc()).all()
    if search:
        search_list = search.split()
        if len(search_list) == 1:
            if search_list[0].isdigit():
                user = User.query.get(search_list[0])
            else:
                user = User.query.filter_by(surname=search_list[0]).first()
        else:
            user = User.query.filter_by(surname=search_list[0]).filter_by(name=search_list[1])
            if len(search_list) == 3:
                user = user.filter_by(patronymic=search_list[2])
            user = user.first()
        if user:
            schedules = user.user_sc
            if not schedules:
                flash('Этот сотрудник не убирался!', category='error')
            else:
                flash(f'Найдено {len(schedules)} расписаний по Вашему запросу!', category='success')
        else:
            flash('Мы не нашли такого сотрудника!', category='error')
    return render_template('index.html', schedules=schedules, User=User, Cabinet=Cabinet)


@app.route('/new_schedule', methods=['POST', 'GET'])
@login_required
def new_schedule():
    if request.method == 'POST':
        cabinet_id = request.form.get('cabinet')
        if request.form.get('auto_date') is not None:
            created_on = ':'.join(str(datetime.now()).split(':')[:-1])  # Получаем текущее время и удаляем секунды
            created_on = datetime.strptime(created_on, "%Y-%m-%d %H:%M")
        else:
            created_on = datetime.strptime(request.form.get('created_date'), "%Y-%m-%dT%H:%M")
        user_id = session['_user_id']
        schedule = ScheduleCleaning(cabinet_id=cabinet_id, user_id=user_id, created_on=created_on)
        db.session.add(schedule)
        db.session.commit()
        flash(f'Расписание кабинета успешно создано!', category='success')
        return redirect(url_for('index'))
    cabinets = Cabinet.query.all()
    return render_template('new_schedule.html', cabinets=cabinets)


@app.route('/new_cabinet', methods=['POST', 'GET'])
@login_required
def new_cabinet():
    if not User.query.get(session['_user_id']).admin_status:
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        cabinet_number = request.form.get('cabinet')
        cabinet = Cabinet(number=cabinet_number)
        db.session.add(cabinet)
        db.session.commit()
        flash(f'Кабинет с номером: {cabinet_number} успешно создан!', category='success')
        return redirect(url_for('index'))
    cabinets = Cabinet.query.all()
    return render_template('new_cabinet.html', cabinets=cabinets)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        surname = request.form.get('surname')
        patronymic = request.form.get('patronymic')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = User.register(username=username, surname=surname, patronymic=patronymic, email=email,
                                 password=password)
            login_user(user)
            flash('Вы успешно зарегистрировались!', category='success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Ошибка регистрации!', category='error')

    return render_template('register.html', all_user=User.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.login_user(username=username, password=password):
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
