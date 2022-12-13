from flask import Blueprint, render_template, request, redirect, flash, jsonify
from flask.helpers import url_for
from flask_login.utils import login_required
from . import db
from .models import Note, Todo
from flask_login import current_user, login_required
import json
# still not working try to fix in future

taskmanager = Blueprint('taskmanager', __name__)

@taskmanager.route('/tasklist', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/tasklist')
        except:
            return 'task was not added bro'
    else:
        # tasks = Todo.query.order_by(user_id=current_user.id).all()
        # tasks=tasks
        return render_template('tasklist.html', user=current_user)

@taskmanager.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('taskmanager.tasks'))
    except:
        return redirect(url_for('taskmanager.tasks'))


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
        return render_template('update.html', task=task, user=current_user)


@taskmanager.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note too short', category='2')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

    return render_template('notes.html', user=current_user)


@taskmanager.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
