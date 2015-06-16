#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

from flask.ext.bootstrap import Bootstrap

from config import config

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)

    from main import main as main_bluepint
    app.register_blueprint(main_bluepint)

    return app

