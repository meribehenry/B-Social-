from app.extensions import bcrypt, db
from sqlalchemy.exc import SQLAlchemyError
from app.services.email_service import EmailService
from app.services.otp_service import OTPService
from app.services.token_service import TokenService
from app.models.user import User
from app.models.profile import Profile
from app.utils.sanitise import sanitise
from flask_jwt_extended import create_access_token, create_refresh_token
from app.utils.response import ServiceResponseBuilder
from app.schemas.user import UserResponseSchema


service_response_builder = ServiceResponseBuilder()
user_response_schema = UserResponseSchema()
otp_service = OTPService()
email_service = EmailService()


class AuthService():
    def __init__(self) -> None:
        self.result = {}
        self.error = {}
    
    def register_user(self, data:dict):
        """ This function register users as unverified to the database"""

        hashed_password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")
        username = sanitise(data.get("email")).split("@")[0]
        email = sanitise(data.get("email"))
        gender = sanitise(data.get("gender"))
        firstname = sanitise(data.get("firstname"))
        lastname = sanitise(data.get("lastname"))


        user_exist = User.query.filter_by(email=email).first()

        # Checks if user already exists and if they are verified 
        if user_exist and user_exist.is_verified:
            self.error = service_response_builder.conflict_error(message="Email already exists")
            return self.result, self.error
        
        # Checks if user already exist and if they aren't verified to delete them
        if user_exist and not user_exist.is_verified:
            try:
                db.session.delete(user_exist)
                db.session.commit() 

            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Sqlalchemy error at auth_service register_user\n{e}")
                self.error = service_response_builder.internal_server_error()
                return self.result, self.error
        
        user = User(username=username, email=email, password=hashed_password, is_verified=False, gender=gender)
        profile = Profile(firstname=firstname, lastname=lastname, user=user)

        try:
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at auth_service register_user\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create account")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at auth_service register_user\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create account")
            return self.result, self.error

        otp = otp_service.generate_otp(email)
        if not otp:
            self.error = service_response_builder.internal_server_error(message="Could not generate otp")
            return self.result, self.error
        
        email_service.send_otp(email, otp)
        email_service.send_welcome_message(email) 

        self.result = service_response_builder.result(message="Account created. Verify email to continue", 
                                                      data=user_response_schema.dump(user))
        
        return self.result, self.error
    

    def login_user(self, data):
        """ This function logs user in"""

        email = sanitise(data.get("email"))
        submitted_password = sanitise(data.get("password"))

        user = User.query.filter_by(email=email).first()

        # Check if user exists or if password is correct 
        if not user or not user.check_password(user.password, submitted_password): 
            self.error = service_response_builder.unauthenticated_error(message="Invalid credential. Please enter the correct email or password")
            return self.result, self.error
        
        # Create access and refresh token
        access_token, refresh_token = create_access_token(identity=str(user.public_id)), \
                                        create_refresh_token(identity=user.public_id)
        
        data = {"user": user_response_schema.dump(user), "access_token": access_token, "refresh_token": refresh_token}
        self.result = service_response_builder.result(message="Successfully logged in", data=data, status_code=201)

        return self.result, self.error
    
    
    def verify_email(self, user_public_id, otp_code):
        """ This function verifies user email and logs them in"""

        user = User.query.filter_by(public_id=user_public_id).first()

        # Check if user exist
        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        
        if otp_service.verify_otp(otp_code, user.email):
            # Create access and refresh token
            access_token, refresh_token = create_access_token(identity=str(user.public_id)), \
                                            create_refresh_token(identity=user.public_id)
            
            data = {"user": user_response_schema.dump(user), "access_token": access_token, "refresh_token": refresh_token}
            self.result = service_response_builder.result(message="You can now explore B-Social", data=data)
            return self.result, self.error
        
        # If otp is invalid
        service_response_builder.validation_error(message="Invalid or expired otp")
        return self.result, self.error


    def reset_password_request(self, data):
        user = User.query.filter_by(email=sanitise(data.get("email"))).first()

        # Check if user exist to send email to them
        if user:
            token_service = TokenService()
            email_service = EmailService()
            token = token_service.generate_reset_token(user.email)
            email_service.send_request_token(token, user.email)

        self.result = service_response_builder.result(message="If the email exist a reset password link has been sent to it",
                                                      status_code=201)

        return  self.result, self.error   

    
    def reset_password(self, data, token):
        token_service = TokenService()
        user = token_service.verify_reset_token(token, max_age=900)

        # Checks if token is verified   
        if not user: 
            self.error = service_response_builder.validation_error(message="Invalid or expired token")
            return  self.result, self.error 

        new_password = sanitise(data.get("password")) 


        # Check if old password is same as new one
        if user.check_password(user.password, new_password):
            self.error = service_response_builder.conflict_error(message="New password cannot be the same as old password")
            return self.result, self.error
        
        user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

        try:
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at auth_service reset_password\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not reset password")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at auth_service reset_password\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not reset password")
            return self.result, self.error 
        
        self.result = service_response_builder.result(message="Password changed successfully. Login to continue")
        return self.result, self.error
     

    def resend_otp(self, user_public_id): 
        user = User.query.filter_by(public_id=user_public_id).first()

        # Check if user exists
        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error

        otp = otp_service.generate_otp(user.email)

        if otp:
            email_service.send_otp(user.email, otp)
            self.result = service_response_builder.result(message="An email containing OTP has been sent to you")
            return self.result, self.error

        # If otp is none
        self.error = service_response_builder.internal_server_error(message="Could not generate otp")
        return self.result, self.error