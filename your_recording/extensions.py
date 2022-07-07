import typing as t
from apiflask import HTTPTokenAuth
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

db = SQLAlchemy()
auth = HTTPTokenAuth()

from .models import User


@auth.verify_token
def verify_token(token: str):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    return user
