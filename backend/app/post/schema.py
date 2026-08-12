from app.extensions import ma
from marshmallow import fields, validate, post_load
import bleach


class NewPostSchema(ma.Schema):
    content = fields.String(load_default="", allow_none=True,
                validate=validate.Length(max=3000, error="Post content cannot exceed 3000 words"))
    
    @post_load
    def sanitize(self, data, **kwarg):

        if data.get("content"):
            data["content"] = bleach.clean(data["content"], tags=[], strip=True).strip()
        return data


class MediaResponseSchema(ma.Schema):
    file_url = fields.String()
    media_type = fields.String()


class PostResponseSchema(ma.Schema):
    public_id = fields.UUID()
    content = fields.String()
    date_created = fields.DateTime(format="iso")
    date_updated = fields.DateTime(format="iso", dump_default=None)
    edited = fields.Boolean()
    num_of_likes = fields.Integer()
    num_of_dislikes = fields.Integer()
    num_of_clicks = fields.Integer()
    num_of_comments = fields.Integer()
    medias = fields.Nested(MediaResponseSchema, many=True, dump_default=[])
    author = fields.Nested("UserResponseSchema", only=("public_id", "username", "profile"))

    