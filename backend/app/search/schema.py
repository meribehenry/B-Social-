from app.extensions import ma
from marshmallow import fields, post_load, post_dump
import bleach


class ProfileSearchSchema(ma.Schema):
    firstname = fields.Str()
    lastname = fields.Str()
    profile_pic_url = fields.Str()


# class PostSearchSchema(ma.Schema):
#     public_id = fields.String()
#     content = fields.String()
#     medias = fields.Nested("MediaResponseSchema")
#     date_created = fields.DateTime(format="iso")
#     date_updated = fields.DateTime(format="iso", dump_default=None)
#     edited = fields.Boolean()
#     num_of_likes = fields.Integer()
#     num_of_dislikes = fields.Integer()
#     num_of_clicks = fields.Integer()
#     num_of_comments = fields.Integer()
#     author = fields.Nested("UserResponseSchema", only=("public_id", "username", "profile"))

    

class SearchUserResponseSchema(ma.Schema):
    public_id = fields.String()  
    username = fields.String()
    status = fields.String()
    profile = fields.Nested(ProfileSearchSchema)
    posts = fields.Nested("PostResponseSchema", many=True, dump_default=[]) 

    @post_dump
    def limit_num_of_posts(self, data, **kwargs):
        data["posts"] = data["posts"][:5]  # Limit to the first 5 posts
        return data


class SearchFieldSchema(ma.Schema):
    search_term = fields.String(required=True)

    @post_load
    def sanitize(self, data, **kwarg):

        if "search_term" in data:
            data["search_term"] = bleach.clean(data["search_term"], tags=[], strip=True).strip()

        return data