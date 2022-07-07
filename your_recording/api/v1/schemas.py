from apiflask import Schema
from apiflask.fields import String, List, Integer, Nested, DateTime


class TokenInSchema(Schema):
    username = String(required=True)
    password = String(required=True)


class TokenOutSchema(Schema):
    token = String()


class UserCreateInSchema(Schema):
    username = String(required=True)
    password = String(required=True)


class LogInSchema(Schema):
    value = Integer()
    item_id = Integer()


class LogOutSchema(Schema):
    id = Integer()
    value = Integer()
    timestamp = DateTime()


class ItemInSchema(Schema):
    name = String(required=True)
    unit = String(required=True)


class ItemOutSchema(Schema):
    id = String()
    name = String()
    unit = String()
    logs = List(Nested(LogOutSchema))


class ItemsOutSchema(Schema):
    items = List(Nested(ItemOutSchema))
