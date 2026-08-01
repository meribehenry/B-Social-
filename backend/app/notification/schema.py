from app.extensions import ma
from marshmallow import fields


class NotificationResponseSchema(ma.Schema):
    recipient = fields.Nested("UserResponseSchema", only=('username', 'public_id'))
    actor = fields.Nested("UserResponseSchema", only=(['profile', 'username', 'public_id']))
    content = fields.String()
    type = fields.String()
    date_created = fields.DateTime(format="iso")


class NotificationStreamResponseSchema(ma.Schema):
    content = fields.String()
    type = fields.String()
    date_created = fields.DateTime(format="iso")