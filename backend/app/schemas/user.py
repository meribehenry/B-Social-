from app.extensions import ma
from marshmallow import fields
from app.schemas.profile import ProfileResponseSchema


class UserResponseSchema(ma.Schema):
    public_id = fields.UUID()
    username = fields.String()
    is_verified = fields.Boolean()
    status = fields.String()
    role = fields.String()
    profile = fields.Nested(ProfileResponseSchema, only=('firstname', 'lastname', 'profile_pic_url'))
    date_joined = fields.DateTime(format="iso")


