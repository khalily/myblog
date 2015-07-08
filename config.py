#!/usr/bin/env python
# encoding: utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'admin@admin.com'
    SUBJECT = "boywyang's blog"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevlopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '371573819@qq.com'
    MAIL_PASSWORD = 'nicaibudao123..'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
            os.path.join(basedir, 'dev-data.sqlite')


class TestingConfig(Config):
    TESTING = True
    ADDONE = 1
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
            os.path.join(basedir, 'test-data.sqlite')


config = {
        'devlopment': DevlopmentConfig,
        'testing': TestingConfig,
        'default': DevlopmentConfig
}

