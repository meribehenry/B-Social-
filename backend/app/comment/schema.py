from app.extensions import ma
from marshmallow import fields, validate, post_load
import bleach


class NewCommentSchema(ma.Schema):
    content = fields.String(load_default=None,
                validate=validate.Length(max=1000, error="Post content cannot exceed 1000 words"))
    
    @post_load
    def sanitize(self, data, **kwarg):
        if "content" in data:
            data["content"] = bleach.clean(data["content"], tags=[], strip=True).strip()
            return data


class CommentResponseSchema(ma.Schema):
    public_id = fields.String()
    content = fields.String()
    date_created = fields.DateTime(format="iso")
    date_updated = fields.DateTime(format="iso")
    edited = fields.Boolean()
    num_of_likes = fields.Integer()
    num_of_dislikes = fields.Integer()
    user = fields.Nested("app.user.schema.UserResponseSchema", only=("public_id", "username", "profile"))

    