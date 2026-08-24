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
                        user:
                          $ref: '#/components/schemas/UserResponse'
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
        description: Login Successful
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
                  example: "Email successfully verified"
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
      404:
        description: Not Found
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NotFoundErrorResponse'
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
              business_logic_error:
                summary: Business Logic Validation Failed
                value:
                  success: false
                  error: "Validation Error"
                  message: "Invalid or expired OTP"
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
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/NotFoundErrorResponse'
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
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ConflictErrorResponse'
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ValidationErrorResponse'
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
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
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ValidationErrorResponse'
      500:
        description: Internal Server Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InternalServerErrorResponse'
    """
    refresh_token = request.cookies.get("refresh_token")

    results, error = auth_service.new_jwt_tokens(refresh_token)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    value=results["data"]["refresh_token"]
    results["data"].pop("refresh_token")

    return api_response.success_extra_data_cookie(
        data=results["data"], message=results.get("message"), status_code=results.get("status_code"), name="refresh_token", value=value)
    
