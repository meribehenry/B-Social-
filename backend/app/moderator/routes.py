from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.moderator.service import ModeratorService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required, moderator_required
from app.moderator.schema import ModeratorTakeDownSchema, ModeratorChangeStatusSchema


moderator_bp = Blueprint("moderator", __name__, url_prefix="/api/v1/moderator")

api_response = APIResponse()


@moderator_bp.route("/posts/<post_public_id>", methods=["POST"])
@jwt_required()
@active_status_required
@moderator_required
def take_down_post(post_public_id):
    """
    Take Down Post Endpoint
    This allows a moderator or an admin to take down a post
    ---
    tags:
      - Moderator
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ModeratorTakeDownRequest'
    responses:
      201:
        description: Successful taken down a post
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Post removed and author has been notified"
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
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "The post does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Post not found"
      403:
        description: Forbidden Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              admin_post_error:
                summary: "Trying to take down the post of an admin"
                value:
                  success: false
                  error: "Forbidden Error"
                  message: "Cannot take down the post of an admin only creator can"
              moderator_post_error:
                summary: "Trying to take down the post of a moderator"
                value:
                  success: false
                  error: "Forbidden Error"
                  message: "Cannot take down the post of your fellow moderator"
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
    """
    try:
        data: [dict] = ModeratorTakeDownSchema().load(request.get_json(silent=True))
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).take_down_post(post_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@moderator_bp.route("/comments/<comment_public_id>", methods=["POST"])
@jwt_required()
@active_status_required
@moderator_required
def take_down_comment(comment_public_id):
    """
    Take Down Comment Endpoint
    This allows a moderator or an admin to take down a comment
    ---
    tags:
      - Moderator
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ModeratorTakeDownRequest'
    responses:
      201:
        description: Successful taken down a comment
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Comment removed and author has been notified"
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
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "The comment does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Comment not found"
      403:
        description: Forbidden Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              admin_comment_error:
                summary: "Trying to take down the comment of an admin"
                value:
                  success: false
                  error: "Forbidden Error"
                  message: "Cannot take down the comment of an admin only creator can"
              moderator_comment_error:
                summary: "Trying to take down the comment of a moderator"
                value:
                  success: false
                  error: "Forbidden Error"
                  message: "Cannot take down the comment of your fellow moderator"
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
    """
    try:
        data: [dict] = ModeratorTakeDownSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).take_down_comment(comment_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@moderator_bp.route("/users/<user_public_id>/", methods=["PATCH"])
@jwt_required()
@active_status_required
@moderator_required
def change_user_status(user_public_id):
    """
    Change User Status Endpoint
    This allows an moderator to change a user status
    ---
    tags:
      - Moderator
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ModeratorChangeStatusRequest'
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
              invalid_credentials:
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
                summary:  A moderator trys to change his or her status
                value:
                  success: false
                  message: "You cannot change your status only admin can, you are a moderator"
                  error: "Validation Error"
              validation_error_2:
                summary:  An moderator enters a wrong password
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
        data: [dict] = ModeratorChangeStatusSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = ModeratorService(get_jwt_identity()).change_user_status(user_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))