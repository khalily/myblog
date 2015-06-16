#!/usr/bin/env python
# encoding: utf-8

from flask import render_template

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main.app_errorhandler(502)
def internal_server_error(e):
    return render_template('errors/502.html'), 502

