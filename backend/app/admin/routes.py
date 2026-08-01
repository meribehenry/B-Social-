from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.admin.service import AdminService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.admin.schema import AdminChangeRoleSchema, AdminChangeStatusSchema


admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

api_response = APIResponse()


@admin_bp.route("/user/<user_public_id>/role", methods=["PATCH"])
@jwt_required()
def change_user_role(user_public_id):
    try:
        data: [dict] = AdminChangeRoleSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = AdminService(get_jwt_identity()).change_user_role(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@admin_bp.route("/users/<user_public_id>/status", methods=["PATCH"])
@jwt_required()
def change_user_status(user_public_id):
    try:
        data: [dict] = AdminChangeStatusSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = AdminService(get_jwt_identity()).change_user_status(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))