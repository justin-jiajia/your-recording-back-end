from your_recording.models import User, Item, Log
from your_recording.extensions import db, auth
from your_recording.api.v1 import api_v1
from your_recording.api.v1.schemas import *
from apiflask import abort


@api_v1.post('/user/')
@api_v1.input(UserCreateInSchema)
@api_v1.output(TokenOutSchema)
def create_user(data):
    if User.query.filter_by(username=data['username']).first():
        abort(400, f'用户名为{ data["username"] }的用户已存在')
    user = User()
    user.username = data['username']
    user.set_password(data['password'])
    token = user.get_token()
    db.session.add(user)
    db.session.commit()
    return {
        'token': f'Bearer {token}'
    }


@api_v1.post('/oath/token/')
@api_v1.input(TokenInSchema)
@api_v1.output(TokenOutSchema)
def get_token(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user.validate_password(data['password']):
        abort(403)
    return {
        'token': f'Bearer {user.get_token()}'
    }


@api_v1.get('/item/')
@api_v1.output(ItemsOutSchema)
@auth.login_required()
def get_user_items():
    return {'items': auth.current_user.items}


@api_v1.get('/item/<int:id>/')
@api_v1.output(ItemOutSchema)
@auth.login_required()
def get_item(id):
    item = Item.query.get_or_404(id)
    if item.author != auth.current_user:
        abort(403)
    return item


@api_v1.delete('/item/<int:id>/')
@api_v1.output(ItemOutSchema)
@auth.login_required()
def delete_item(id):
    item = Item.query.get_or_404(id)
    if item.author != auth.current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    return '', 204


@api_v1.post('/item/')
@api_v1.input(ItemInSchema)
@api_v1.output(ItemsOutSchema)
@auth.login_required()
def create_item(data):
    item = Item()
    item.name = data['name']
    item.unit = data['unit']
    item.author = auth.current_user
    db.session.add(item)
    db.session.commit()
    return {'items': auth.current_user.items}


@api_v1.get('/log/<int:id>/')
@api_v1.output(LogOutSchema)
@auth.login_required()
def get_log(id):
    log = Log.query.get_or_404(id)
    if log.item.author != auth.current_user:
        abort(403)
    return log


@api_v1.delete('/log/<int:id>/')
@auth.login_required()
def delete_log(id):
    log = Log.query.get_or_404(id)
    if log.item.author != auth.current_user:
        abort(403)
    db.session.delete(log)
    db.session.commit()
    return '', 204


@api_v1.post('/log/')
@api_v1.input(LogInSchema)
@api_v1.output(ItemOutSchema)
@auth.login_required()
def create_log(data):
    item = Item.query.get_or_404(data['item_id'])
    if item.author != auth.current_user:
        abort(403)
    log = Log()
    log.value = data['value']
    log.item = item
    db.session.add(log)
    db.session.commit()
    return Item.query.get(data['item_id'])
