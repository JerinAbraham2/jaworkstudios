from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
#os means operating system

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    #how you initialize flask
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pasdjapsodnhof bsiudfiusdfbisdf'

    #datbase auth
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    #change later if you need it:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    #registering blueprints
    from .views import views
    from .auth import auth
    from .taskmanager import taskmanager

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(taskmanager, url_prefix='/')

    #check database and make database if not there
    from .models import User, Note, Todo
    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Database made')

