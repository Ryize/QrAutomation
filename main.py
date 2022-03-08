from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    name_user = 'John Johnovich'
    all_users = ['Charly', 'Matt', 'Richard', 'Kany']
    return render_template('index.html', user=name_user, all_users=all_users)


@app.route('/register/hi')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run()
