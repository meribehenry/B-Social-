from flask import Blueprint, request
from flask_jwt_extended import get_jwt,  jwt_required
from app.auth.services.auth_service import AuthService
from marshmallow import ValidationError
from app.auth.schema import LoginSchema, RegistrationSchema, VerifyEmailSchema, ResetPasswordSchema, ResetPasswordRequestSchema
from app.shared.response import APIResponse
from app.extensions import limiter


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

auth_service = AuthService()
api_response = APIResponse()


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per minute")
def register():
    """
    User Registration Endpoint
    Registers a user
    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/RegistrationRequest'
    responses:
      200:
        description: Verify email to continue. This response is sent when the user trys to register again immediately after registering while they have not verified their email
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Verify email to continue"
                    data: 
                      type: object
                      properties:
                        is_verified: 
                          type: boolean
                          example: false
                        profile:
                          type: object
                          properties:
                            firstname: 
                              type: string
                              example: "Meribe"
                            lastname:
                              type: string
                              example: "Henry"
                            profile_pic_url:
                              type: string
                              example: "default.jpg"
                            bio:
                              type: string
                              example: ""
                        role:
                          type: string
                          example: "user"
                        status:
                          type: string
                          example: "active"
                        username:
                          type: string
                          example: "meribehenry"
                        public_id:
                          type: string
                          example: "02dbc4da-cacb-4a8e-9b9e-8e8bbdaaa964"
                        date_joined:
                          type: datetime
                          format: iso
                          example: "2026-08-11T13:50:10.902126"
      201:
        description: Account created
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Account created. Please verify email to continue"
                    data: 
                      type: object
                      properties:
                        is_verified: 
                          type: boolean
                          example: false
                        profile:
                          type: object
                          properties:
                            firstname: 
                              type: string
                              example: "Meribe"
                            lastname:
                              type: string
                              example: "Henry"
                            profile_pic_url:
                              type: string
                              example: "default.jpg"
                            bio:
                              type: string
                              example: ""
                        role:
                          type: string
                          example: "user"
                        status:
                          type: string
                          example: "active"
                        username:
                          type: string
                          example: "meribehenry"
                        public_id:
                          type: string
                          example: "02dbc4da-cacb-4a8e-9b9e-8e8bbdaaa964"
                        date_joined:
                          type: datetime
                          format: iso
                          example: "2026-08-11T13:50:10.902126"
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "Email already exist"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Email already exist"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    email: 
                      - "Field must not be empty"
      429:
        description: Rate Limit Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RateLimitErrorResponse'
            
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
            examples:
              request_failed:
                summary: "Request failed"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not create account"
    """

    try:
        data = RegistrationSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.register_user(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    """
    User Login Endpoint
    Authenticate an existing user
    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/LoginRequest'
    responses:
      200:
        description: Logged In Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Successfully logged in"
                    data:
                      type: object
                      properties:
                        access_token:
                          type: string 
                          example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4NjYxMjczMSwianRpIjoiMTVlM2Y2ZjktYTcyNy00YTIzLWIxYjItMjFkZGM3OGRkODM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFmOTY4MTAxLTIwOWMtNDE0MC05Y2M3LTZlMDgwMmY3M2VlOCIsIm5iZiI6MTc4NjYxMjczMSwiY3NyZiI6IjNmYjYxMWM1LTFmYTItNGRkOC05YTJkLTE3YjQzMzA4YzY3MiIsImV4cCI6MTc4NjYxOTkzMX0.mrkSLjEB3eXAm2R5Ivh89X3MNnpoe-PHVpVPjWZtZ3g"
                        user:
                          $ref: '#/components/schemas/UserResponse'
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
      401:
        description: Unauthenticated Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "Wrong email or password"
                value:
                  success: false
                  error: "Unauthenticated error"
                  message: "Invalid Credentials. Please enter the correct email or password"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    email: 
                      - "Field must not be empty"
      429:
        description: Rate Limit Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RateLimitErrorResponse'
            
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """
    
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.login_user(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
  
    value = results["data"]["refresh_token"]
    results["data"].pop("refresh_token")

    return api_response.success_extra_data_cookie(
        data=results["data"], message=results.get("message"), status_code=results.get("status_code"), name="refresh_token", value=value)
    

@auth_bp.route("/users/<user_public_id>/email", methods=["PATCH"])
def verify_email(user_public_id):

    """
    Verify Email Endpoint
    Verifies users email
    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/VerifyEmailRequest'
    responses:
      200:
        description: Successfully verified email
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "You can now explore B-Social"
                data:
                  type: object
                  properties:
                    access_token:
                      type: string
                      example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4NjYxMjczMSwianRpIjoiMTVlM2Y2ZjktYTcyNy00YTIzLWIxYjItMjFkZGM3OGRkODM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFmOTY4MTAxLTIwOWMtNDE0MC05Y2M3LTZlMDgwMmY3M2VlOCIsIm5iZiI6MTc4NjYxMjczMSwiY3NyZiI6IjNmYjYxMWM1LTFmYTItNGRkOC05YTJkLTE3YjQzMzA4YzY3MiIsImV4cCI6MTc4NjYxOTkzMX0.mrkSLjEB3eXAm2R5Ivh89X3MNnpoe-PHVpVPjWZtZ3g"
                    user:
                      $ref: '#/components/schemas/UserResponseSchema'                 
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "The user does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "User not found"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    otp_code: 
                      - "Field must not be empty"
      429:
        description: Rate Limit Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RateLimitErrorResponse'
            
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """
    try:
        data = VerifyEmailSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.verify_email(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    value=results["data"]["refresh_token"]
    results["data"].pop("refresh_token")
  
    return api_response.success_extra_data_cookie(
        data=results["data"], message=results.get("message"), status_code=results.get("status_code"), name="refresh_token", value=value)
        
    
@auth_bp.route("/otp/users/<user_public_id>", methods=["POST"])
@limiter.limit("4 per minute")
def resend_otp(user_public_id):
    """
    Resend OTP Endpoint
    Sends OTP to users email
    ---
    tags:
      - Authentication
    responses:
      201:
        description: Login Successful
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "An email containing OTP has been sent to you"          
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "The user does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "User not found"
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """
    results, error = auth_service.resend_otp(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/reset/request", methods=["POST"])
@limiter.limit("10 per minute")
def reset_request():
    """
    Reset Password Request Endpoint
    Sends reset password link to users email
    ---
    tags:
      - Authentication
    requestBody:
      required: True
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/RequestPasswordResetRequest'
    responses:
      201:
        description: If the email exist a reset password link has been sent to it 
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "If the email exist a reset password link has been sent to it"
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """    
    try:
        data = ResetPasswordRequestSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.reset_password_request(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@auth_bp.route("/reset/password/<token>", methods=["PATCH"])
def reset_password(token):
    """
    Reset Password Endpoint
    Resets users password
    ---
    tags:
      - Authentication
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/PasswordResetRequest'
    responses:
      200:
        description: Password successfully changed
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Password changed successfully. Login to continue"
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "New password matches old password"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "New password cannot be the same as old password"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    password: 
                      - "Field must not be empty"
      429:
        description: Rate Limit Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RateLimitErrorResponse'
            
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
            examples:
              request_failed:
                summary: "Failed to reset password"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not create password"
    """
    try:
        data = ResetPasswordSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.reset_password(data, token)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout Endpoint
    Logs out a user by blocking the access token and refresh token 
    ---
    tags:
      - Authentication
    responses:
      200:
        description: Logout Successful
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "Successfully logged out"
      401:
        description: Unauthenticated Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "Expired or bad refresh token"
                value:
                  success: false
                  error: "Unauthenticated error"
                  message: "Refresh token expired"            
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    password: 
                      - "Field must not be empty"
              no_refresh_token:
                summary: Missing refresh token
                value:
                  success: false
                  message: "Refresh token missing"
                  error: "Validation error"
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """

    access_token_jti = get_jwt().get("jti")
    refresh_token = request.cookies.get("refresh_token")

    results, error = auth_service.logout_user(access_token_jti, refresh_token)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/refresh", methods=["POST"])
# @jwt_required(refresh=True, locations=["headers", "cookies"])
def get_new_jwt_tokens():
    """
    Refresh Tokens Endpoint
    Gives a user new access and refresh token
    ---
    tags:
      - Authentication 
    responses:
      200:
        description: Tokens created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: "New access and refresh token created"
                data:
                  type: object
                  properties:
                    access_token:
                      type: string
                      example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4NjYxMjczMSwianRpIjoiMTVlM2Y2ZjktYTcyNy00YTIzLWIxYjItMjFkZGM3OGRkODM2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjFmOTY4MTAxLTIwOWMtNDE0MC05Y2M3LTZlMDgwMmY3M2VlOCIsIm5iZiI6MTc4NjYxMjczMSwiY3NyZiI6IjNmYjYxMWM1LTFmYTItNGRkOC05YTJkLTE3YjQzMzA4YzY3MiIsImV4cCI6MTc4NjYxOTkzMX0.mrkSLjEB3eXAm2R5Ivh89X3MNnpoe-PHVpVPjWZtZ3g"
      401:
        description: Unauthenticated Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "Expired or bad refresh token"
                value:
                  success: false
                  error: "Unauthenticated error"
                  message: "Refresh token expired"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              marshmallow_error:
                summary:  Schema validation failed (Marshmallow)
                value:
                  success: false
                  message: "Input validation failed"
                  errors: 
                    password: 
                      - "Field must not be empty"
              no_refresh_token:
                summary: Missing refresh token
                value:
                  success: false
                  message: "Refresh token missing"
                  error: "Validation error"
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
            examples:
              request_failed:
                summary: "Request failed"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not generate new jwt tokens"
    """
    refresh_token = request.cookies.get("refresh_token")

    results, error = auth_service.new_jwt_tokens(refresh_token)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    value=results["data"]["refresh_token"]
    results["data"].pop("refresh_token")

    return api_response.success_extra_data_cookie(
        data=results["data"], message=results.get("message"), status_code=results.get("status_code"), name="refresh_token", value=value)
    
