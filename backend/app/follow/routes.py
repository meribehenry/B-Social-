from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.follow.service import FollowerService
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required


follow_bp = Blueprint("follow", __name__, url_prefix="/api/v1/")

api_response = APIResponse()


@follow_bp.route("/users/<user_public_id>/follow", methods=["POST"])
@jwt_required()
@active_status_required
def follow(user_public_id):
    """
    Follow User Endpoint
    This allows users to follow another user
    ---
    tags:
      - Follow
    responses:
      201:
        description: Successful followed user
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Successfully followed user"
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
                summary: "Already following user"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Already following user"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              follow_error:
                summary:  Cannot follow yourself
                value:
                  success: false
                  message: "Input validation failed"
                  error: "Validation error"
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
                summary: "Failed to follow user"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not follow user"
    """
    results, error = FollowerService(get_jwt_identity()).follow_user(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/follow", methods=["DELETE"])
@jwt_required()
@active_status_required
def unfollow(user_public_id):
    """
    Unfollow User Endpoint
    This allows users to unfollow another user
    ---
    tags:
      - Follow
    responses:
      200:
        description: Successful unfollowed user
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Successfully unfollowed user"
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
                summary: "Already unfollowed user"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Already unfollowed user"
      422:
        description: Validation Error
        content:
          application/json:
            schema:
              oneOf:
                - $ref: '#/components/schemas/ErrorResponse'
                - $ref: '#/components/schemas/SchemaErrorResponse'
            examples:
              follow_error:
                summary:  Cannot follow yourself
                value:
                  success: false
                  message: "Input validation failed"
                  error: "Validation error"
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
                summary: "Failed to unfollow"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not unfollow user"
    """
    results, error = FollowerService(get_jwt_identity()).unfollow_user(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/followers", methods=["GET"])
@jwt_required()
@active_status_required
def view_followers(user_public_id):
    """
    View Followers Endpoint
    This allows a user view all the their followers or other users followers
    ---
    tags:
      - Follow
    responses:
      200:
        description: Followers Sent
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
                      type: object
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
                summary: "The user does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "User not found"
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

    results, error = FollowerService(get_jwt_identity()).get_followers_or_followings(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/following", methods=["GET"])
@jwt_required()
@active_status_required
def view_following(user_public_id):
    """
    View Followings Endpoint
    This allows a user view all the their followings or other users followings
    ---
    tags:
      - Follow
    responses:
      200:
        description: Followings Sent
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
                      type: object
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
                summary: "The user does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "User not found"
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

    results, error = FollowerService(get_jwt_identity()).get_followers_or_followings(user_public_id, get_type="following")

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/following/list", methods=["GET"])
@jwt_required()
@active_status_required
def get_following_users_public_id_list(user_public_id):
    """
    Get Followings List Endpoint
    This allows a user to get the list of public ids of users they follow. This is to be used for rendering state in the frontend 
    ---
    tags:
      - Follow
    responses:
      200:
        description: Followings list Sent
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
                      type: object
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
    results, error = FollowerService(get_jwt_identity()).get_following_users_public_id_list()
    
    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))