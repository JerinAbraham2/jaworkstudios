================================app.py backup==========================================
import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pydatabase.db'
db = SQLAlchemy(app)

#redirects http:// to https://
@app.before_request
def before_request():
    if 'DYNO' in os.environ:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #think this is automatic as well
    content = db.Column(db.String(200), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #automatic

    def __repr__(self):
        return '<Task %r>' % self.id

#activate database (if you change your database stuff maybe trying doing this again)
#go into your env, then type python3 to go into the python shell (this thing: '>>>>')
#from app import db
#db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/tasklist', methods=['GET', 'POST'])
def tasklist():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/tasklist')
        except:
            return 'task was not added bro'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('tasklist.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/tasklist')
    except:
        return 'hey bro '

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/tasklist')
        except:
            return 'redirect'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)



#web app: source /home/tobidendom/Documents/py/pyflask/env/bin/activate


#first time making new app or something pip3 install virtualenv (or just pip)
#once your in the virtual enviroment using the below source env/bin/activate
#then type in that pip3 (or just pip again) install flask (in linux you can do sudo apt install flask i think im not sure, i think you have to do pip and under env)
#same thing if you want sqlalchemy for that env, install in that env again using pip- install pip install flask-sqlalchemy


#the regular is below:
#run this: source env/bin/activate then flask run

    # cant have comments in the html if you have a base.html <!--you can use this for javascript as well <link rel="stylesheet" href="{{ url_for('static', filename='css/index.css') }}"> -->
    # <!-- the above is ginger {} text {{}} and it will take the thing and give the return as a string or something  -->
    # <!-- you cant have comments in the pages that inherit the base.html -->


#updating website git
#heroku login (or login heroku?)
#git add .
#git commit -m "comment here about what your changing"
#git push heroku master
================================app.py backup==========================================



====================index.html backup=====================================
{% extends "base.html" %}

{% block title %}
    <title>JAWORKS Website</title> 
{% endblock %}

{% block main %}
    <!-- Hero section -->
    <div class="hero" id="home">
        <div class="hero__container">
            <h1 class="hero__heading">Welcome to
                <span>
                    Jaworks
                </span>
            </h1>
            <p class="hero__description">Unlimited possibilities</p>
            <button class="main__btn"><a href="#">Explore</a></button>
        </div>
    </div>
    <!-- About section -->
    <div class="main" id="about">
        <div class="main__container">
            <div class="main__img--container">
                <div class="main__img--card"><i class="fas fa-layer-group"></i></div>
            </div>
            <div class="main__content">
                <h1>What is our goal?</h1>
                <h2>Useful services and products</h2>
                <p>Email our CEO to learn more about our services</p>
                <button class="main__btn"><a href="#">Email CEO</a></button>
            </div>
        </div>
    </div>

    <!-- Services section -->
    <div class="services" id="services">
        <h1>Our services</h1>
        <div class="services__wrapper">
            <a class="services__card">
                <h2>Custom JAWORKS projects</h2>
                <p>Soon to be working on a JA-AI (or Jaworks AI for longer)</p>
                <div class="services__btn"><button>Get started</button></div>
            </a>
            <a class="services__card" href="{{ url_for('tasklist') }}">
                <h2>Useful utilities</h2>
                <p>Many projects</p>
                <div class="services__btn"><button>Get started</button></div>
            </a>
            <a class="services__card">
                <h2>Fun games</h2>
                <p>Explore the created games</p>
                <div class="services__btn"><button>Get started</button></div>
            </a>
            <a class="services__card">
                <h2>Graphical user interfaces</h2>
                <p>Available on windows, mac and linux</p>
                <!-- you put an image tag here if you want to replace with images or somewhere -->
                <div class="services__btn"><button>Get started</button></div>
            </a>
        </div>
    </div>

    <!-- features section -->
    <div class="main" id="sign-up">
        <div class="main__container">
            <div class="main__content">
                <h1>Join our team</h1>
                <h2>Sign up today</h2>
                <p>Proud supporters:</p>
                <p>- butterysmooth</p>
                <button class="main__btn"><a href="#">Sign up</a></button>
            </div>
            <div class="main__img--container">
                <div class="main__img--card" id="card-2"><i class="fas fa-users"></i></div>
            </div>
        </div>
    </div>
{% endblock %}


====================index.html backup=====================================




====================tasklist.html backup=====================================
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div class="content">
        <h1>Task master</h1>
        {% if tasks|length < 1 %}
        <h4>Create a task below:</h4>
        {% else %}
        <table class="table">
            <tr>
                <th>Task</th>
                <th>Added</th>
                <th>Actions</th>
            </tr>
            {% for task in tasks %}
            <tr>
                <td>{{ task.content }}</td>
                <td>{{ task.date_created.date() }}</td>
                <td>
                    <a href="/delete/{{task.id}}">Delete</a>
                    <br>
                    <a href="/update/{{task.id}}">Update</a>

                </td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
        <div class="form">
            <form action="/tasklist" method="POST">
                <input type="text" name="content" id="content">
                <input type="submit" value="Add task">
            </form>
        </div>
        <a href="/">return to jaworks</a>
    </div>
</body>
</html>


====================tasklist.html backup=====================================