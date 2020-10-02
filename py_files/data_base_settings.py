#!/usr/bin/env python3
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False
engine = create_engine('sqlite:///./database.db')
db = SQLAlchemy(app)


def find_or_create_database():
    for file in os.listdir("./"):
        if file.endswith(".db"):
            return
    db.create_all()


def find_users_in_database(user_list):
    if type(user_list) is str:
        if any(char.isalpha() for char in user_list) is True:
            result = db.session.query(User).filter(User.username == user_list).first()
            if result is None:
                return False
            else:
                return True
        user_integer = int(user_list)
        result = db.session.query(User).get(user_integer)
        if result is None:
            return False
    else:
        for user in user_list:
            user_integer = int(user)
            result = db.session.query(User).get(user_integer)
            if result is None:
                return False
    return True


association_table = db.Table('Users_chats',
                             db.Column('user_id', db.Integer, db.ForeignKey('Users.id')),
                             db.Column('chat_id', db.Integer, db.ForeignKey('Chats.id'))
                             )


class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)


class Chat(db.Model):
    __tablename__ = 'Chats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', secondary=association_table, backref='Chats', lazy='dynamic')
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)


class Message(db.Model):
    __tablename__ = 'Messages'
    id = db.Column(db.Integer, primary_key=True)
    chat = db.Column(db.Integer, db.ForeignKey('Chats.id'))
    author = db.Column(db.Integer, db.ForeignKey('Users.id'))
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
