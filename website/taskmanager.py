from flask import Blueprint, request, redirect, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from website import create_app

taskmanager = Blueprint('taskmanager', __name__)
current_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pydatabase.db'

db = SQLAlchemy(current_app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #think this is automatic as well
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) #automatic
    def __repr__(self):
        return '<Task %r>' % self.id

@taskmanager.route('/tasklist', methods=['GET', 'POST'])
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

@taskmanager.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/tasklist')
    except:
        return 'hey bro '

@taskmanager.route('/update/<int:id>', methods=['GET','POST'])
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