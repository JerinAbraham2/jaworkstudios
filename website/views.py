from flask import Blueprint, render_template
from flask_login import current_user
#this file is a blueprint of our application, it has a bunch of routes and urls inside of it

views = Blueprint('views', __name__)

#route of homepage
@views.route('/')
def home():
    return render_template('home.html', user=current_user)

@views.route('/slideshow')
def slideshow():
    return render_template('slideshow.html', user=current_user)

