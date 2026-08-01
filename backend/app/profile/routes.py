from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.profile.service import ProfileService
from app.shared.response import APIResponse
from marshmallow import ValidationError
from app.profile.schema import EditProfileSchema


profile_bp = Blueprint("profile", __name__, url_prefix="/api/v1/")

api_response = APIResponse()


@profile_bp.route("/users/<user_public_id>/profile", methods=["GET"])
@jwt_required()
def view_profile(user_public_id):
    results, error = ProfileService(get_jwt_identity()).view_profile(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@profile_bp.route("/users/<user_public_id>/profile", methods=["PATCH"])
@jwt_required()
def edit_profile(user_public_id):
    try:
        data: [dict] = EditProfileSchema().load(request.form)
        print(data)
        file = request.files.get("file")
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = ProfileService(get_jwt_identity()).edit_profile(user_public_id, data, file)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))