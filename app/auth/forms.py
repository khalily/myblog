from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo, Regexp, ValidationError
from ..models import User
from flask.ext.login import current_user


class LoginForm(Form):
    email = StringField("Email", validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField("Password", validators=[Required(), Length(1, 16)])
    remember_me = BooleanField("Keep me Login in")
    submit = SubmitField("Login in")


class RegisterForm(Form):
    email = StringField("Email", validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField("UserName", validators=[Required(), Length(1, 64),
                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          "UserName must have only letters, numbers,"
                                          "dots or underscores")])
    password = PasswordField("Password", validators=[Required(), Length(1, 16),
                                EqualTo('password2', message="Password must match.")])
    password2 = PasswordField("Confirm Password", validators=[Required()])
    submit = SubmitField("Register")

    def validate_email(self, field):
       if User.query.filter_by(email=field.data).first():
           raise ValidationError("Email Already registered.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username Already in use.")


class ChangePasswordForm(Form):
    old_password = PasswordField('old password', validators=[Required(), Length(1, 16)])
    new_password = PasswordField('new password', validators=[Required(), Length(1, 16),
                                 EqualTo('confirm_password', 'two password must consist')])
    confirm_password = PasswordField('confirm password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('Change')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Old password incorrect')


class ResetPasswordRequestForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email incorrect')


class ResetPasswordForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64), Email()])
    new_password = PasswordField('new_password', validators=[Required(), Length(1, 16),
                                 EqualTo('confirm_password', 'two password must consist')])
    confirm_password = PasswordField('confirm_password', validators=[Required(), Length(1, 16)])
    submit = SubmitField('submit')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Email incorrect')

class ChangeEmail(Form):
    verify_password = PasswordField('verify password', validators=[Required(), Length(1, 16)])
    new_email = StringField('new email', validators=[Required(), Length(1, 64), Email()])
    submit = SubmitField('Submit')

    def validate_verify_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Password incorrect')

    def validate_new_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already in use')
