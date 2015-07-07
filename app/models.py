#!/usr/bin/env python
# encoding: utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from . import db
from . import login_manager



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)

    pending_email = db.Column(db.String(64), unique=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return "<User %r>" % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        return True

    def generate_change_email_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        self.email = self.pending_email
        db.session.add(self)
        db.session.commit()
        return True

    def can(self, permissions):
        return self.role is not None and \
           (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    users = db.relationship("User", backref="role", lazy="dynamic")

    @staticmethod
    def insert_roles():
        roles = {
            "User": (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            "Moderator": (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            "Administrator": (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return "<Role> %r" % self.name


class Permission:
    FOLLOW = 0x1
    COMMENT = 0x2
    WRITE_ARTICLES = 0x4
    MODERATE_COMMENTS = 0x8
    ADMINISTER = 0x80

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
