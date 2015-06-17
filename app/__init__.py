#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from main import main as main_bluepint
    app.register_blueprint(main_bluepint)

    from auth import auth as auth_bluepint
    app.register_blueprint(auth_bluepint, url_prefix='/auth')

    return app

