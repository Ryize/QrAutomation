from flask import render_template, request, flash

from main import app


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if len(request.form.get('password')) < 4:
            1/0
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
