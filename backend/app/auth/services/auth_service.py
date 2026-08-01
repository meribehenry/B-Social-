from app.extensions import bcrypt, db
from app.shared.services.email_service import EmailService
from app.auth.services.otp_service import OTPService
from app.auth.services.auth_token_service import TokenService
from app.user.model import User
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app.shared.response import ServiceResponseBuilder
from app.user.schema import UserResponseSchema
from app.user.service import UserService


service_response_builder = ServiceResponseBuilder()
user_response_schema = UserResponseSchema()
otp_service = OTPService()
email_service = EmailService()
auth_token_service = TokenService()
user_service = UserService()


class AuthService():
    def __init__(self) -> None:
        self.result = {}
        self.error = {}
    
    def register_user(self, data:dict):
        """ 
        This function register users as unverified to the database. Data must be the dictionary returned by RegristrationSchema for user to be
        created. It returns already serislized user as response data
        """

        hashed_password = bcrypt.generate_password_hash(data.get("password")).decode("utf-8")
        username = data.get("email").split("@")[0]
        email = data.get("email")
        gender = data.get("gender")
        firstname = data.get("firstname")
        lastname = data.get("lastname")


        user_exist = user_service.get_user_object(email, retrival_method="email")

        # Checks if user already exists and if they are verified 
        if user_exist and user_exist.is_verified:
            self.error = service_response_builder.conflict_error(message="Email already exists")
            return self.result, self.error
        
        # Checks if user already exist and if they aren't verified to delete them
        if user_exist and not user_exist.is_verified:
           user_service.delete_user(user_exist.email, retrival_method="email")
        
        # Create a new user
        user = user_service.create_new_user(email, hashed_password, username, firstname, lastname, gender)

        # Check user was created
        if not user: 
            self.error = service_response_builder.internal_server_error(message="Could not create account")
            return self.result, self.error

        otp = otp_service.generate_otp(email)

        # Checks if otp was generated
        if not otp:
            self.error = service_response_builder.internal_server_error(message="Could not generate otp")
            return self.result, self.error
        
        print("OTP generated successfully")
        # Send emails
        email_service.send_welcome_message(email) 
        email_service.send_otp(email, otp)
        print(f"OTP generated for {email} is {otp}")

        self.result = service_response_builder.result(message="Account created. Verify email to continue", 
                                                      data=user_response_schema.dump(user))
        
        return self.result, self.error
    

    def login_user(self, data:dict):
        """ This function logs user in"""

        email = data.get("email")
        submitted_password = data.get("password")

        user = user_service.get_user_object(email, retrival_method="email")

        # Check if user exists or if password is correct 
        if not user or not user.check_password(submitted_password): 
            self.error = service_response_builder.unauthenticated_error(message="Invalid credential. Please enter the correct email or password")
            return self.result, self.error
        
        # Create access and refresh token
        access_token, refresh_token = create_access_token(identity=str(user.public_id)), \
                                        create_refresh_token(identity=user.public_id)
        
        data = {"user": user_response_schema.dump(user), "access_token": access_token, "refresh_token": refresh_token}
        self.result = service_response_builder.result(message="Successfully logged in", data=data, status_code=201)

        return self.result, self.error
    
    
    def verify_email(self, user_public_id, data:dict):
        """ This function verifies user email and logs them in. Returs already serilized user response data"""

        user = user_service.get_user_object(user_public_id)

        # Check if user exist
        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        otp_code = data.get("otp_code")

        if otp_service.verify_otp(otp_code, user.email):
            user_service.mark_user_email_has_verified(user.email, retrival_method="email")

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
        email = data.get("email")
        user = user_service.get_user_object(email, retrival_method="email", return_bool=True)

        # Check if user exist to send email to them
        if user:
            token = auth_token_service.generate_reset_token(email)
            email_service.send_request_token(token, email)

        self.result = service_response_builder.result(message="If the email exist a reset password link has been sent to it",
                                                      status_code=201)

        return  self.result, self.error   

    
    def reset_password(self, data, token):

        # Checks if token is verified
        user = auth_token_service.verify_reset_token(token, max_age=900)
        if not user: 
            self.error = service_response_builder.validation_error(message="Invalid or expired token")
            return self.result, self.error 

        new_password = data.get("password")

        # Check if old password is same as new one
        if user.check_password(user.password, new_password):
            self.error = service_response_builder.conflict_error(message="New password cannot be the same as old password")
            return self.result, self.error
        
        new_hashed_password = bcrypt.generate_password_hash(new_password) # Hash new password

        # Change user password and check if it changed
        if user_service.change_user_password(new_hashed_password, user.email, retrival_method="email"):
            self.result = service_response_builder.result(message="Password changed successfully. Login to continue")
            return self.result, self.error

        self.error = service_response_builder.internal_server_error(message="Could not reset password")
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
    

    def logout_user(self, access_token_jti, refresh_token):
        
        try:
            # Decode refresh token to get the payload
            refresh_token_jti = decode_token(refresh_token).get("jti")
        except Exception as e:
            print(f"An error at auth_service logout\n{e}")
            self.error = service_response_builder.validation_error(message="Could not validate refresh token")
            return self.result, self.error
        
        # Block both the refresh and access token
        if auth_token_service.block_jwt_token(access_token_jti, refresh_token_jti):
            self.result = service_response_builder.result(message="Successfully logged out")
            return self.result, self.error
        
        else:
            self.error = service_response_builder.internal_server_error(message="Could not logout")
            return self.result, self.error
           
    
    def new_jwt_tokens(self, user_public_id, refresh_token_jti):
        
        # Create access and refresh token
        access_token, refresh_token = create_access_token(identity=str(user_public_id)), \
                                        create_refresh_token(identity=user_public_id)
        
        
        # Block the refresh token used to generate the new jwt tokens
        if auth_token_service.block_jwt_token(refresh_token_jti=refresh_token_jti):
            self.result = service_response_builder.result(message="Successfully logged out")
            data = {"access_token": access_token, "refresh_token": refresh_token}

            self.result = service_response_builder.result(message="New jwt tokens created", data=data, status_code=201)
            return self.result, self.error
        
        else:
            self.error = service_response_builder.internal_server_error(message="Could generate new jwt tokens")
            return self.result, self.error