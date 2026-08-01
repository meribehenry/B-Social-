from flask import Blueprint, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.auth.services.auth_service import AuthService
from marshmallow import ValidationError
from app.auth.schema import LoginSchema, RegistrationSchema, VerifyEmailSchema, ResetPasswordSchema, ResetPasswordRequestSchema
from app.shared.response import APIResponse


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

auth_service = AuthService()
api_response = APIResponse()


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = RegistrationSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.register_user(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = LoginSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.login_user(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@auth_bp.route("/verify_email/<user_public_id>", methods=["PATCH"])
def verify_email(user_public_id):
    try:
        data = VerifyEmailSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.verify_email(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/resend_otp/<user_public_id>", methods=["POST"])
def resend_otp(user_public_id):
    results, error = auth_service.resend_otp(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/reset_request", methods=["POST"])
def reset_request():
    try:
        data = ResetPasswordRequestSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = auth_service.reset_password_request(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@auth_bp.route("/reset_password/<token>", methods=["PATCH"])
def reset_password(token):
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
    access_token_jti = get_jwt().get("jti")
    refresh_token = request.get_json(silent=True)

    results, error = auth_service.logout_user(access_token_jti, refresh_token)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def get_new_jwt_tokens():
    refresh_token_jti = get_jwt().get("jti")
    results, error = auth_service.new_jwt_tokens(get_jwt_identity(), refresh_token_jti)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))