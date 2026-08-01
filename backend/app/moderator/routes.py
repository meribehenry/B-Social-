from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.moderator.service import ModeratorService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.moderator.schema import ModeratorTakeDownSchema, ModeratorChangeStatusSchema


moderator_bp = Blueprint("moderator", __name__, url_prefix="/api/v1/moderator")

api_response = APIResponse()


@moderator_bp.route("/posts/<post_public_id>", methods=["DELETE"])
@jwt_required()
def take_down_post(post_public_id):
    try:
        data: [dict] = ModeratorTakeDownSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).take_down_post(post_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@moderator_bp.route("/comments/<comment_public_id>", methods=["DELETE"])
@jwt_required()
def take_down_comment(comment_public_id):
    try:
        data: [dict] = ModeratorTakeDownSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).take_down_comment(comment_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@moderator_bp.route("/user/<user_public_id>/status", methods=["PATCH"])
@jwt_required()
def change_user_status(user_public_id):
    try:
        data: [dict] = ModeratorChangeStatusSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).change_user_status(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))