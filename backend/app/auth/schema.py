from app.extensions import ma
from marshmallow import fields, validate, validates, validates_schema, ValidationError, post_load
import re
import bleach


class RegistrationSchema(ma.Schema):
   
    email = fields.Email(required=True,
            error_messages={"required": "Email is required", "invalid": "Invalid email"})
               
    firstname = fields.String(required=True,
                validate=validate.Length(min=2, max=20, error="Firstname length must be 2-20 characters long"))
               
               
    lastname = fields.String(required=True,
                validate=validate.Length(min=2, max=20, error="Lastname length must be 2-20 characters long"))
                               
    password = fields.String(required=True,
                load_only=True)
    
    confirm_password = fields.String(required=True,
                load_only=True)
               
    gender = fields.String(required=True)
    
    
    @validates("gender")
    def validate_gender_correct(self, value, **kwarg):
        if value.lower() not in ["male", "female"]:
            raise ValidationError("Gender value not valid", "gender")
    
    @validates_schema
    def validate_password(self, data, **kwarg):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long", "password")

        if password != confirm_password:
            raise ValidationError("Password does not match", "confirm_password")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain lowercase letter")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain uppercase letter")

        
    @validates_schema
    def validate_names_isalnum(self, data, **kwarg):
        firstname = data.get("firstname")
        lastname = data.get("lastname")

        if not firstname.isalnum():
            raise ValidationError("Fields must be alphanumeric", "firstname")
        
        if not lastname.isalnum():
            raise ValidationError("Fields must be alphanumeric", "lastname")
    
    @post_load
    def sanitise(self, data, **kwarg):
        fields_to_sanitise = ["firstname", "lastname", "username", "gender", "password", "confirm_password"]

        for field in fields_to_sanitise:
            if field in data:
                data[field] = bleach.clean(data[field], tags=[], strip=True).strip()
        return data

           
class LoginSchema(ma.Schema):
    email = fields.Email(required=True,
            error_messages={"required": "Email is required", "invalid": "Invalid email"})
                              
    password = fields.String(required=True,
                validate=validate.Length(min=8, error="Password length atleast 8 characters long"),
                load_only=True)
    
    @post_load
    def sanitize(self, data, **kwarg):
        if "password" in data:
            data["password"] = bleach.clean(data["password"], tags=[], strip=True).strip()
        return data


class VerifyEmailSchema(ma.Schema):
    otp_code = fields.Integer(required=True, load_only=True)


class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True, load_only=True)
    
    confirm_password = fields.String(required=True, load_only=True)
    
    @validates_schema
    def validate_password(self, data, **kwarg):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long", "password")

        if password != confirm_password:
            raise ValidationError("Password does not match", "confirm_password")
        
        if password != confirm_password:
            raise ValidationError("Password does not match", "confirm_password")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain uppercase letter")
        
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain lowercase letter")

        if not re.search(r'[0-9]', password):
            raise ValidationError("Password must contain uppercase letter")
        
        
    @post_load
    def sanitise(self, data, **kwarg):
        fields_to_sanitise = ["password", "confirm_password"]

        for field in fields_to_sanitise:
            if field in data:
                data[field] = bleach.clean(data[field], tags=[], strip=True).strip()
        return data


class ResetPasswordRequestSchema(ma.Schema):
    email = fields.Email(required=True,
            error_messages={"required": "Email is required", "invalid": "Invalid email"})