from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='1')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='2')
        else:
            flash('email does not exist.', category='2')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        displayName = request.form.get('displayName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='2')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='2')
        elif len(displayName) < 2:
            flash('Display name must be greater than 2 characters', category='2')
        elif password1 != password2:
            flash('Passwords don\'t match', category='2')
        elif len(password1) > 7:
            flash('Password length must be less than 7', category='2')
        else:
            new_user = User(email=email, display_name=displayName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created', category='1')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)

