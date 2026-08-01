from app.extensions import ma
from marshmallow import fields, validate, validates_schema, ValidationError, post_load
import bleach

class ProfileResponseSchema(ma.Schema):
    firstname = fields.String()
    lastname = fields.String()
    bio = fields.String()
    user = fields.Nested("app.user.schema.UserResponseSchema", only=("public_id", "username", "date_joined"))
    profile_pic_url = fields.String()
    num_of_posts = fields.Integer()
    num_of_followers = fields.Integer()
    num_of_followings = fields.Integer()


class EditProfileSchema(ma.Schema):
    firstname = fields.String(load_default="", allow_none=True)
    lastname = fields.String(load_default="", allow_none=True)
    username =fields.String(load_default="", allow_none=True, validate=validate.Length(max=20, error="Username length must be less than 20 characters"))
    bio = fields.String(load_default="", validate=validate.Length(max=500, error="Bio length must be less than 500 characters"))
    
    @validates_schema
    def validate_names_isalnum(self, data, **kwarg):
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        if firstname and not firstname.isalnum():
            raise ValidationError("Fields must be alphanumeric", "firstname")
        
        if lastname and not lastname.isalnum():
            raise ValidationError("Fields must be alphanumeric", "lastname")

    @post_load
    def sanitise(self, data, **kwarg):
        fields_to_sanitise = ["firstname", "lastname", "username", "bio"]

        for field in fields_to_sanitise:
            if field in data and data[field] is not None:
                data[field] = bleach.clean(data[field], tags=[], strip=True).strip()
        return data