from datetime import datetime

from flask import render_template, request, flash, url_for, redirect, session

from app import app, db
from models import User, Cabinet, ScheduleCleaning
from flask_login import login_required, logout_user

from error_controller import *

from werkzeug.wrappers.response import Response


def _get_date() -> datetime:
    """
    Получает дату для расписания, переданную пользователем.
    Если стоит автоматическое определние, то функция сама получает дату
    """
    if request.form.get('auto_date') is not None:
        created_on = ':'.join(str(datetime.now()).split(':')[:-1])  # Получаем текущее время и удаляем секунды
        created_on = datetime.strptime(created_on, "%Y-%m-%d %H:%M")
    else:
        created_on = datetime.strptime(request.form.get('created_date'), "%Y-%m-%dT%H:%M")
    return created_on


def _create_schedule(cabinet_id: int) -> Response:
    """
    Функция для создания нового расписания. Получение даты происходит с помощью _get_date()
    Возвращает ссылку для перехода на главную страницу(Функция: index)
    """
    created_on = _get_date()
    user_id = session['_user_id']
    schedule = ScheduleCleaning(cabinet_id=cabinet_id, user_id=user_id, created_on=created_on)
    db.session.add(schedule)
    db.session.commit()
    flash(f'Расписание кабинета успешно создано!', category='success')
    print(type(redirect(url_for('index'))))
    return redirect(url_for('index'))


def check_admin_status() -> bool:
    """
    Проверяет является ли пользователем Администратором(С помощью сессии: session['_user_id'])
    """
    if User.query.get(session['_user_id']).admin_status:
        return True
    return False


def get_user_info(user: User = None) -> str:
    """
    Функция для получения информации по пользователю(Его id, ФИО, почта).
    :return: str(В строке уже записаны все данные)
    """
    if not user:
        user = User.query.get(session['_user_id'])
    return f"(id: {user.id}). {user.surname} {user.name} {user.patronymic}(Почта: {user.email})"


def auth_user() -> bool:
    """ Функция проверяет авторизован ли пользователь """
    return bool(session['_user_id'])


@app.route('/')
@app.route('/schedules')
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
                flash('Этот сотрудник не создавал расписаний!', category='error')
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
        app.logger.info(f"Создано новое расписание для кабинета: {cabinet_id}. Создал(а): {get_user_info()}")
        return _create_schedule(cabinet_id)
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('new_schedule.html', cabinets=cabinets)


@app.route('/delete_schedule', methods=['GET'])
@login_required
def delete_schedule():
    if not check_admin_status():
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        app.logger.warning(f"Сотрудник с недостаточным уровнем допуска попытался удалить расписание: {get_user_info()}")
        return redirect(url_for('index'))
    schedule_id = request.args.get('schedule_id')

    ScheduleCleaning.query.filter_by(id=schedule_id).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/new_schedule/<cabinet_number>', methods=['POST', 'GET'])
@login_required
def new_schedule_id(cabinet_number):
    if request.method == 'POST':
        cabinet_id = Cabinet.query.filter_by(number=cabinet_number).first().id
        app.logger.info(f"Создано новое расписание: {cabinet_number}. Создал(а): {get_user_info()}")
        return _create_schedule(cabinet_id)
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('new_schedule.html', cabinets=cabinets, cabinet_number=cabinet_number)


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
            flash('Вы успешно зарегистрировались!', category='success')
            app.logger.info(f"Зарегестрирован новый аккаунт: {get_user_info(user)}.")
            return redirect(url_for('index'))
        except ValueError:
            flash('Ошибка регистрации!', category='error')

    return render_template('auth/register.html', all_user=User.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.login_user(username=username, password=password):
            return redirect(url_for('index'))
        else:
            flash('Ошибка авторизации!', category='error')

    return render_template('auth/login.html')


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