from werkzeug.security import generate_password_hash, check_password_hash
from authlib.jose import jwt
from flask import current_app
from datetime import datetime
from .extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    items = db.relationship('Item', back_populates='author', cascade='all')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self):
        header = {'alg': 'HS256'}
        payload = {
            'id': self.id
        }
        return jwt.encode(
            header, payload, str(current_app.config['SECRET_KEY'])
        ).decode()


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    unit = db.Column(db.String(5))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='items')
    logs = db.relationship('Log', back_populates='item', cascade='all')


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    item = db.relationship('Item', back_populates='logs')
