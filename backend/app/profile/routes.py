from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.profile.service import ProfileService
from app.shared.response import APIResponse
from marshmallow import ValidationError
from app.profile.schema import EditProfileSchema
from app.shared.decorators import active_status_required


profile_bp = Blueprint("profile", __name__, url_prefix="/api/v1/")

api_response = APIResponse()


@profile_bp.route("/users/<user_public_id>/profile", methods=["GET"])
@jwt_required()
@active_status_required
def view_profile(user_public_id):
    """
    View Profile Endpoint
    Allows a user to view other users profile 
    ---
    tags:
      - Profile
    responses:
      200:
        description: Profile Sent
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
                  example: ""
                data:
                  $ref: '#/components/schemas/ProfileResponseSchema'
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
    results, error = ProfileService(get_jwt_identity()).view_profile(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@profile_bp.route("/users/<user_public_id>/profile", methods=["PATCH"])
@jwt_required()
@active_status_required
def edit_profile(user_public_id):
    """
    Edit Profile Endpoint
    This allows users to edit their profile
    ---
    tags:
      - Profile
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/EditProfileRequest'
    responses:
      200:
        description: Profile updated Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Profile successfully updated"
                    data:
                      $ref: '#/components/schemas/ProfileResponseSchema'
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
            examples:
              max_file_exceeded:
                summary: "Exceeded maximum number of files you can send"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Only four files are supported max"
              non_file_or_content_sent:
                summary: "No file or other field was sent"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Invalid request. Please enter atleast one field"
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
                summary: "Unauthorised to edit this profile"
                value:
                  success: false
                  error: "Forbidden error"
                  message: "You are not authorized to edit this profile"
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              not_found:
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
              already_exists:
                summary: "Username already exists"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Username already exists"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              bad_file_type:
                summary:  When the file sent is not in the allowed extension
                value:
                  success: false
                  message: "Invalid file type. Please enter the correct type: [jpg, img, jpeg, png]"
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
                summary: "Failed to update profile"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not update profile"
    """
    try:
        data: [dict] = EditProfileSchema().load(request.form)
        files = request.files
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = ProfileService(get_jwt_identity()).edit_profile(user_public_id, data, files)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))