#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user, login_required

from . import auth
from forms import LoginForm, RegisterForm, ChangePasswordForm
from ..models import User, db
from ..email import send_email


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,
                 password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(form.email.data, 'confirm', 'email/confirm',
                   user=user, token=token)
        flash("We have send email to your email, please confirm to complete register")
        return redirect(url_for('.login'))
    return render_template("auth/register.html", form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash("you have confirm your account")
    else:
        flash("Invalidated confirm")
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'confirm', 'email/confirm',
               token=token, user=current_user)
    flash('a new conformation email send to your email')
    return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    print current_user.confirmed
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(password=form.password.data):
            flash("login successful!")
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('user not exists or password error')
    return render_template("auth/login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('change_password')
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.add(current_user)
        db.session.commit()
        flash('your password change successful.')
        return redirect('main.index')
    return render_template('auth/change_password.html', form=form)

