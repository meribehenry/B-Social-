from app.extensions import ma
from marshmallow import fields, validate, validates, validates_schema, ValidationError
from app.models.user import User
import re


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
   
   
    # @validates("email")
    # def validate_email_unique(self, value, **kwarg):
    #     user = User.query.filter_by(email=value).first()
       
    #     if user:
    #         raise ValidationError(f"Email '{value}' already exist")
    
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
        
        if not lastname.isaplnum():
            raise ValidationError("Fields must be alphanumeric", "lastname")

           
class LoginSchema(ma.Schema):
    email = fields.Email(required=True,
            error_messages={"required": "Email is required", "invalid": "Invalid email"})
                              
    password = fields.String(required=True,
                validate=validate.Length(min=8, error="Password length atleast 8 characters long"),
                load_only=True)


class VerifyEmailSchema(ma.Schema):
    otp_code = fields.Integer(required=True, load_only=True)

class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True,
                load_only=True)
    
    confirm_password = fields.String(required=True,
                load_only=True)
    
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


class ResetRequestSchema(ma.Schema):
    email = fields.Email(required=True,
            error_messages={"required": "Email is required", "invalid": "Invalid email"})