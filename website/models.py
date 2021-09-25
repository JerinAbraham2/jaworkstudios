from . import db
#from . means from this package (from init.py i think) equivelant if it was somewhere else like website like import website import db or something
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #this does it for you, you don't have to do it (maybe)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))#foreign key references another primary key in another model (maybe. not sure, maybe not a rule) one to many, one user with many notes
                                                #user here is the class(lowercase in sql) and the .id is the column (maybe)
# foreign keys only work in a one to many relationship, 1 user having many notes (I think)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True) #unique = true means no one else can have another email the same (maybe)
    password = db.Column(db.String(150))
    display_name = db.Column(db.String(150))
    notes = db.relationship('Note')#tell flask and sql everytime you make a notes add it into the user notes relationship that note id (I think) (here you do need capital for sql (maybe))
    todo = db.relationship('Todo')
    def is_active(self):
        return True

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True) #think this is automatic as well
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow()) #automatic
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #adding this todo model
    def __repr__(self):
        return '<Task %r>' % self.id