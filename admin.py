from app import app, db, SITE_URL
from controller import check_admin_status
from flask import flash, request, redirect, render_template, url_for, send_file
from flask_login import login_required
from models import *
from controller import get_user_info
from PIL import Image, ImageDraw

import os
import qrcode


def generate_qr_code(id: str) -> str:
    """
    Функция генерирует qr код в который вшита ссылка для создания нового кабинета
    Пример: http://127.0.0.1/new_schedule/2.18
    qr код сохраняется в папку qrCodes в виде png картинки(Пример такого файла: 'Кабинет: 2.18.png')
    """
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


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_index():
    if not check_admin_status():
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        app.logger.warning(
            f"Сотрудник с недостаточным уровнем допуска попытался войти в админ-панель: {get_user_info()}")
        return redirect(url_for('index'))
    users = User.query.all()
    cabinets = Cabinet.query.all()
    return render_template('admin/index.html', users=users, cabinets=cabinets)


@app.route('/work_with_user', methods=['GET', 'POST'])
@login_required
def work_with_user():
    if not check_admin_status():
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        app.logger.warning(
            f"Сотрудник с недостаточным уровнем допуска попытался удалить пользователя: {get_user_info()}")
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.filter_by(id=int(user_id))
        user_list = User.query.get(user_id)
        flash(f'Сотрудник: (id {user_list.id}) {user_list.surname} {user_list.name} {user_list.patronymic} успешно удалён!', category='success')
        user.delete()
        db.session.commit()
    users = User.query.order_by(User.admin_status.desc()).order_by(User.surname).all()
    return render_template('admin/work_with_user.html', users=users)


@app.route('/admin/new_cabinet_qr/', methods=['POST', 'GET'])
@login_required
def new_cabinet_qr():
    if not check_admin_status():
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        app.logger.warning(f"Сотрудник с недостаточным уровнем допуска попытался создать qr код: {get_user_info()}")
        return redirect(url_for('index'))
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
            app.logger.info(f"Создан новый qr код для кабинета: {cabinet_number}. Создал(а): {get_user_info()}")
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('admin/new_cabinet_qr.html', cabinets=cabinets)


@app.route('/admin/new_cabinet', methods=['POST', 'GET'])
@login_required
def new_cabinet():
    if not check_admin_status():
        flash(f'У вас нет прав для просмотра данной страницы!', category='error')
        app.logger.warning(f"Сотрудник с недостаточным уровнем допуска попытался создать кабинет: {get_user_info()}")
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
        app.logger.info(f"Создан новый кабинет: {cabinet_number}. Создал(а): {get_user_info()}")
        return redirect(url_for('index'))
    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('admin/new_cabinet.html', cabinets=cabinets)


@app.route('/admin/delete_cabinet', methods=['GET', 'POST'])
@login_required
def delete_cabinet():
    if request.method == 'POST':
        if not check_admin_status():
            flash(f'У вас нет прав для просмотра данной страницы!', category='error')
            app.logger.warning(
                f"Сотрудник с недостаточным уровнем допуска попытался удалить кабинет: {get_user_info()}")
            return redirect(url_for('index'))
        cabinet_id = request.form.get('cabinet')

        Cabinet.query.filter_by(id=cabinet_id).delete()
        db.session.commit()
        flash(f'Кабинет успешно удалён!', category='success')
        return redirect(url_for('index'))

    cabinets = Cabinet.query.order_by(Cabinet.number).all()
    return render_template('admin/delete_cabinet.html', cabinets=cabinets)
