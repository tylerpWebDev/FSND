import os
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
from flask import jsonify


database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    print("Dropping database and recreating")
    db.drop_all()
    db.create_all()


class Movies(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=False)
    release_date = Column(DateTime, default=datetime.utcnow)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def __repr__(self):
        return '"id": "{self.id}", "title": "{self.title}", "release_date": "{self.release_date}" '.format(self=self)


class Actor(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False)
    age = Column(Integer(), unique=False)
    gender = Column(String(6), unique=False)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def update(self):
        db.session.commit()

    def __repr__(self):
        return '"id": "{self.id}", "name": "{self.name}", "age": "{self.age}", "gender": "{self.gender}"'.format(self=self)
