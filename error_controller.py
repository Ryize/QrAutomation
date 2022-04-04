from flask import render_template

from app import app


@app.errorhandler(404)
def error404(error):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def error500(error):
    app.logger.critical(f"Возникла ошибка 500!!!")
    return render_template('error/500.html'), 500
