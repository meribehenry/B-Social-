from app.extensions import ma
from marshmallow import fields, validate
from app.schemas.user import UserResponseSchema


class NewPostSchema(ma.Schema):
    content = fields.String(load_default=None,
                validate=validate.Length(max=3000, error="Post content cannot exceed 3000 words"))



class PostResponseSchema(ma.Schema):
    public_id = fields.UUID()
    content = fields.String()
    post_type = fields.String()
    media_url = fields.String()
    date_created = fields.DateTime(format="iso")
    date_updated = fields.DateTime(format="iso", dump_default=None)
    edited = fields.Boolean()
    num_of_likes = fields.Integer()
    num_of_dislikes = fields.Integer()
    num_of_clicks = fields.Integer()
    num_of_comments = fields.Integer()
    user = fields.Nested(UserResponseSchema, only=("public_id", "username", "profile"))
    