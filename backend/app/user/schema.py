from app.extensions import ma
from marshmallow import fields


class UserResponseSchema(ma.Schema):
    public_id = fields.String()
    username = fields.String()
    is_verified = fields.Boolean()
    status = fields.String()
    role = fields.String()
    profile = fields.Nested("ProfileResponseSchema", only=('firstname', 'lastname', 'profile_pic_url'))
    date_joined = fields.DateTime(format="iso")


