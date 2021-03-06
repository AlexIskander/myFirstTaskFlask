from flask import Flask
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import Required
from app import db
from app.models import User, Question, Answer
from werkzeug.security import generate_password_hash, check_password_hash

class LoginForm(Form):
    login    = TextField('login',  validators = [Required()])
    password = PasswordField('password', validators=[Required()])

    def validate_login(self, field):
        user = self.get_user()
        if user is None:
            raise validators.ValidationError('Invalid user or password')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid user or password')

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


from wtforms import BooleanField, TextField, PasswordField, validators

def validate_login(self, field):
    if db.session.query(User).filter_by(login=self.username.data).count() > 0:
        raise validators.ValidationError('Duplicate username')

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25), validate_login])
    email    = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm    = PasswordField('Repeat Password')


class questionForm(Form) :
    question   = TextAreaField(u'Your question', [validators.optional(), validators.length(max=200)])


class answerForm(Form) :
    answer  = TextAreaField(u'add your answer', [validators.optional(), validators.length(max=200)])
    vote    = BooleanField( default=False) 



