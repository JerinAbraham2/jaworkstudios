import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pydatabase.db'
db = SQLAlchemy(app)



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

@app.before_request
def before_request():
    if 'DYNO' in os.environ:
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


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
    app.run(debug=False)



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
