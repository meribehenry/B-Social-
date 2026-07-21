from app.extensions import ma
from app.schemas.user import UserResponseSchema
from marshmallow import fields, validate, validates_schema, ValidationError

class ProfileResponseSchema(ma.Schema):
    firstname = fields.String()
    lastname = fields.String()
    bio = fields.String()
    user = fields.Nested(UserResponseSchema, only=("public_id", "username", "data_joined"))
    profile_pic_url = fields.String()
    num_of_posts = fields.Integer()
    num_of_followers = fields.Integer()
    num_of_followings = fields.Integer()


class EditProfileSchema(ma.Schema):
    firstname = fields.String(load_default=None)
    lastname = fields.String(load_default=None)
    bio = fields.String(load_default=None, validate=validate.Length(max=500, error="Bio length must be less than 500 characters"))
    

    @validates_schema
    def validate_names_isalnum(self, data, **kwarg):
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        if not firstname.isalnum():
            raise ValidationError("Fields must be alphanumeric", "firstname")
        
        if not lastname.isaplnum():
            raise ValidationError("Fields must be alphanumeric", "lastname")
    


