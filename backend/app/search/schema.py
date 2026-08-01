from app.extensions import ma
from marshmallow import fields, post_load
import bleach


class SearchResponseSchema(ma.Schema):
    public_id = fields.String()
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
    author = fields.Nested("UserResponseSchema", only=("public_id", "username", "profile"))


class SearchFieldSchema(ma.Schema):
    search_term = fields.String(required=True)

    @post_load
    def sanitize(self, data, **kwarg):

        if "search_term" in data:
            data["search_term"] = bleach.clean(data["search_term"], tags=[], strip=True).strip()

        return data