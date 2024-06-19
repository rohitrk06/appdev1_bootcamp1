# from flask import current_app as app , redirect, render_template, url_for
from main import app
from flask import render_template

@app.route("/")
def index():
    return render_template('index.html')