from app.extensions import ma
from marshmallow import fields
from app.schemas.user import UserResponseSchema


class NotificationResponseSchema(ma.Schema):
    recipient = fields.Nested(UserResponseSchema, only=('username', 'public_id'))
    actor = fields.Nested(UserResponseSchema, only=('username', 'public_id'))
    type = fields.String()
    date_created = fields.String()
    is_read = fields.Boolean()