#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, url_for, request, abort
from flask.ext.login import current_user
from . import main


@main.before_app_request
def before_request():
    if not request.endpoint:
        abort(404)
    if current_user.is_authenticated() \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@main.route('/')
def index():
    test = "<h1>HAHA</h1>"
    return render_template('index.html', test=test)

