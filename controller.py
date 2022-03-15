from flask import render_template, request, flash, session, make_response, url_for

from main import app


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

    name_user = 'John Johnovich'
    all_users = ['Charly', 'Matt', 'Richard', 'Kany']
    return render_template('index.html', user=name_user, all_users=all_users)


@app.route('/register')
def register():
    return render_template('register.html')


@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'), 404
