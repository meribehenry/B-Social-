from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.admin.service import AdminService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.shared.decorators import admin_required, active_status_required
from app.admin.schema import AdminChangeRoleSchema, AdminChangeStatusSchema


admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

api_response = APIResponse()


@admin_bp.route("/users/<username>/role", methods=["PATCH"])
@jwt_required()
@active_status_required
@admin_required
def change_user_role(username):
    """
    Change User Role Endpoint
    This allows an admin to change a user role
    ---
    tags:
      - Admin
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AdminChangeRoleRequest'
    responses:
      200:
        description: Role Changed Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "User role has been changed"
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
                summary: "Expired JWT token"
                value:
                  success: false
                  error: "Unauthenticated error"
                  message: "Please login to continue"
      403:
        description: Forbidden Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              forbidden_errror:
                summary: "Unauthorised to change a user role"
                value:
                  success: false
                  error: "Forbidden error"
                  message: "You cannot change role of an admin or make a user an admin, only the creator can"
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
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "The user already has the role"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "User already has this role"
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
              validation_error_1:
                summary:  An admin trys to change his or her role
                value:
                  success: false
                  message: "You cannot change your role you are an admin"
                  error: "Validation Error"
              validation_error_2:
                summary:  An admin enters a wrong password
                value:
                  success: false
                  message: "Invalid password. Please enter a correct password"
                  error: "Validation Error"
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
                summary: "Failed to change user role"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not change user role"
    """
    
    try:
        data: [dict] = AdminChangeRoleSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = AdminService(get_jwt_identity()).change_user_role(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@admin_bp.route("/users/<user_public_id>/status", methods=["PATCH"])
@jwt_required()
@active_status_required
@admin_required
def change_user_status(user_public_id):
    """
    Change User Status Endpoint
    This allows an admin to change a user status
    ---
    tags:
      - Admin
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/AdminChangeStatusRequest'
    responses:
      200:
        description: Status Changed Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "User status has been changed"
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
                summary: "Expired JWT token"
                value:
                  success: false
                  error: "Unauthenticated error"
                  message: "Please login to continue"
      403:
        description: Forbidden Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              forbidden_error:
                summary: "Unauthorised to change a user status"
                value:
                  success: false
                  error: "Forbidden error"
                  message: "You cannot change status of an admin only the creator can"
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
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              invalid_credentials:
                summary: "The user already has the status"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "User already has this status"
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
              validation_error_1:
                summary:  An admin trys to change his or her status
                value:
                  success: false
                  message: "You cannot change your status you are an admin"
                  error: "Validation Error"
              validation_error_2:
                summary:  An admin enters a wrong password
                value:
                  success: false
                  message: "Invalid password. Please enter a correct password"
                  error: "Validation Error"
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
                summary: "Failed to change user status"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not change user status"
    """
    try:
        data: [dict] = AdminChangeStatusSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = AdminService(get_jwt_identity()).change_user_status(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))