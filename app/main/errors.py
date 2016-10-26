from . import main
from flask import render_template

@main.app_errorhandler(404)
def page404(e):
    return render_template('404.html'), 404
