# -*- coding: utf-8 -*-

import os
import datetime
from app import app
from flask import Flask, render_template, request, session, g, redirect, url_for, abort,  render_template, flash
from forms import LoginForm, RegistrationForm, questionForm, answerForm
from flask.ext.login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Question, Answer
from app import db
from flask.ext.login import current_user, login_user, logout_user, login_required
from sqlalchemy import update

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))


@app.route('/')
@app.route('/index')
def index():
    questions = db.session.query(Question).all()     
    return render_template('index.html', title="Home", questions=questions )


@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    user = form.login.data 
    if request.method == 'POST' and form.validate_on_submit():
        user = db.session.query(User).filter_by(login=form.login.data).first()
        login_user(user) 
        return redirect('/index')     
    return render_template('login.html', title="Login", form=form, user=user )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(login = form.username.data, email = form.email.data, password = generate_password_hash(form.password.data) )
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form,  )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/index')


@app.route("/question",  methods = ['GET', 'POST'] )
@login_required
def question():    
    form = questionForm()
    if request.method == 'POST' and form.validate():
        now_date = datetime.datetime.now() 
        question = Question(text=form.question.data, timestamp=now_date, user_id=request.form['user_id']  )
        db.session.add(question)
        db.session.commit()
        return redirect('/index')
    return render_template('question.html', form=form )


@app.route("/post/<int:post_id>", methods = ['GET', 'POST'])
def show_post(post_id):
    form = answerForm()
    if request.method == 'POST' and form.validate():
        now_date = datetime.datetime.now() 
        answer = Answer(text_answer=form.answer.data, timestamp=now_date, user_id=request.form['user_id'],
                           question_id=request.form['question_id']  )
        db.session.add(answer)
        db.session.commit()
        return redirect('/post/%d' % post_id)
    post   = db.session.query(Question).filter_by( id=post_id)
    answer = db.session.query(Answer).filter_by( question_id=post_id)
    return  render_template('post.html', post_id=post_id, post=post, form=form, answer=answer )


@app.route("/add_vote", methods = ['GET', 'POST'])
def add_vote():
    if request.method == 'POST':
        vote = request.form['vote']
        u = db.session.query(Answer).get(vote)
        x = 0 if u.vote == None else u.vote 
        u.vote = x + 1
        db.session.commit()
        return 'Thank you for voting'
    return  'not ok'



