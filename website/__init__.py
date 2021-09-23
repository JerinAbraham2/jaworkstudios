import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def create_app():
    #how you initialize flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pasdjapsodnhof bsiudfiusdfbisdf'

    #registering blueprints
    from .views import views
    from .auth import auth
    # from .taskmanager import taskmanager

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # app.register_blueprint(taskmanager, url_prefix='/')

    return app

