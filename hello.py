#!/usr/bin/env python
# encoding: utf-8

from datetime import datetime

from flask import Flask
from flask import redirect, render_template
from flask import abort

from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return "<h1>Hello World!</h1>"

@app.route('/user/<name>')
def user(name):
    return render_template("index.html", name=name,
            current_time=datetime.utcnow())

@app.route('/getuser/<id>')
def get_user(id):
    abort(404)

@app.route('/redirect')
def redirect_google():
    return redirect("http://www.google.com")

if __name__ == "__main__":
    app.run(debug=True)

