from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.shared.response import APIResponse
from app.user.service import UserService

user_bp = Blueprint("users",  __name__, url_prefix="/api/v1/users")


api_response = APIResponse()

@user_bp.route("/<user_public_id>", methods=["GET"])
@jwt_required()
def get_user(user_public_id):
    """
    User Endpoint
    This endpoint is used to get a particular user
    ---
    tags:
      - User
    responses:
      200:
        description: User Sent
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: ""
                    data:
                      $ref: '#/components/schemas/UserResponseSchema'
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

    results, error = UserService().get_user(get_jwt_identity())

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))

    return api_response.success(data=results["data"], message=results.get("message"), status_code=results.get("status_code"))