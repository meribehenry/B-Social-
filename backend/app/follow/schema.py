from app.extensions import ma
from marshmallow import fields


class FollowersResponseSchema(ma.Schema):
    public_id = fields.UUID()
    username = fields.String()
    status = fields.String()
    profile = fields.Nested("ProfileResponseSchema", only=('firstname', 'lastname', 'profile_pic_url'))


class FollowersResponseSchema2(ma.Schema):
    public_id = fields.String()
    follower = fields.Nested("UserResponseSchema", only=('username', 'public_id', 'profile'))
    followed_user = fields.Nested("UserResponseSchema", only=('username', 'public_id'))
    followed_at = fields.DateTime(format="iso")
    