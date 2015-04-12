#Imports the blueprint and defines the routes associated
#with authentication
from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

#Route decorator for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    #create object of LoginForm defined in auth/forms.py
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #Checks whether authenticated user or not
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

#Route decorator for logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

#Route decorator for logout
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    #Ensures whether every field follows the form convention
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        #Adds into session which is stored in cookies
        db.session.add(user)
        flash('You can now login.')
        #Redirects to Login page after successfully Registration 
        return redirect(url_for('auth.login'))
    #In case your field did not follow convention
    return render_template('auth/register.html', form=form)
