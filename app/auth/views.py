#!/usr/bin/env python
# encoding: utf-8

from flask import render_template
from . import auth


@auth.route('/register')
def register():
    pass

@auth.route('/login')
def login():
    return render_template("login.html")

