from datetime import datetime

from flask import render_template, request, flash, url_for, redirect, session, send_file

from app import app, db, SITE_URL
from models import User, Cabinet, ScheduleCleaning
from flask_login import login_required, logout_user, login_user
from PIL import Image, ImageDraw

from error_controller import *

import qrcode
import os


def _get_date():
    if request.form.get('auto_date') is not None:
        created_on = ':'.join(str(datetime.now()).split(':')[:-1])  # Получаем текущее время и удаляем секунды
        created_on = datetime.strptime(created_on, "%Y-%m-%d %H:%M")
    else:
        created_on = datetime.strptime(request.form.get('created_date'), "%Y-%m-%dT%H:%M")
    return created_on


def _create_schedule(cabinet_id):
    created_on = _get_date()
    user_id = session['_user_id']
    schedule = ScheduleCleaning(cabinet_id=cabinet_id, user_id=user_id, created_on=created_on)
    db.session.add(schedule)
    db.session.commit()
    flash(f'Расписание кабинета успешно создано!', category='success')
    return redirect(url_for('index'))


def generate_qr_code(id: str):
    data = f'http://{SITE_URL}/new_schedule/{id}'
    file_path = f"qrCodes/Кабинет: {id}.png"
    img = qrcode.make(data)
    img.save(file_path)

    image = Image.open(file_path)

    drawer = ImageDraw.Draw(image)
    drawer.text((10, 0), f"CABINET: {id}", fill='black')

    os.remove(file_path)

    image.save(file_path)
    image.show()

    return file_path


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
        return _create_schedule(cabinet_id)
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('new_schedule.html', cabinets=cabinets)


@app.route('/new_schedule/<cabinet_number>', methods=['POST', 'GET'])
@login_required
def new_schedule_id(cabinet_number):
    if request.method == 'POST':
        cabinet_id = Cabinet.query.filter_by(number=cabinet_number).first().id
        return _create_schedule(cabinet_id)
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('new_schedule.html', cabinets=cabinets, cabinet_number=cabinet_number)


@app.route('/new_cabinet_qr/', methods=['POST', 'GET'])
@login_required
def new_cabinet_qr():
    if request.method == 'POST':
        cabinet_number = request.form.get('cabinet')
        if not len(cabinet_number.split('.')) == 2:
            flash(f'Номер кабинета должен разделятся точкой(Пример: 1.27)!', category='error')
            return redirect(url_for('index'))
        file_path = generate_qr_code(cabinet_number)
        try:
            return send_file(file_path, as_attachment=True)
        finally:
            os.remove(file_path)
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('new_cabinet_qr.html', cabinets=cabinets)


@app.route('/new_cabinet', methods=['POST', 'GET'])
@login_required
def new_cabinet():
    if not User.query.get(session['_user_id']).admin_status:
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        cabinet_number = request.form.get('cabinet')
        if not len(cabinet_number.split('.')) == 2:
            flash(f'Номер кабинета должен разделятся точкой(Пример: 1.27)!', category='error')
            return redirect(url_for('index'))
        cabinet = Cabinet(number=cabinet_number)
        db.session.add(cabinet)
        db.session.commit()
        flash(f'Кабинет с номером: {cabinet_number} успешно создан!', category='success')
        return redirect(url_for('index'))
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
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
