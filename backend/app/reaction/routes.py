from flask import Blueprint, request
from app.reaction.schema import ReactionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.reaction.service import PostReactionService, CommentReactionService
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required


reactions_bp = Blueprint("reactions", __name__, url_prefix="/api/v1/")

api_response = APIResponse()
reaction_schema = ReactionSchema()


@reactions_bp.route("/posts/<post_public_id>/reactions", methods=["POST"])
@jwt_required()
@active_status_required
def react_to_post(post_public_id):
    """
    React to Post Endpoint
    This allows users to react to a post
    ---
    tags:
      - Reaction
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ReactionRequest'
    responses:
      200:
        description: Reaction changed Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Changed to liked"
                    data:
                      type: object
      201:
        description: Reaction created Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Post liked"
                    data:
                      type: object
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
            examples:
              invalid_reaction_type:
                summary: "Invalid reaction type"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Invalid reaction type must be either (like) or (dislike)"
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
              not_found:
                summary: "The post does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Post not found"
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "Already have that reaction to a particular post"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Post already liked"
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
                    reaction_type: 
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
            examples:
              request_failed:
                summary: "Failed to react to post"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not react to  post"
    """
    try:
        data: [dict] = reaction_schema.load(request.get_json(silent=True))
        pass
    except ValidationError as e:
        return api_response.schema_error(e.messages)
    
    results, error = PostReactionService(get_jwt_identity()).toggle_reaction(post_public_id,  data.get("reaction_type"))

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("/posts/<post_public_id>/reactions", methods=["DELETE"])
@jwt_required()
@active_status_required
def remove_post_reaction(post_public_id):
    """
    Remove Post Reaction Endpoint
    This allows users to remove the reaction they made to a post
    ---
    tags:
      - Reaction
    responses:
      200:
        description: Reaction removed Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Reaction removed"
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
              post_not_found:
                summary: "The post does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Post not found"
              reaction_not_found:
                summary: "The reaction does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Reaction not found" 
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
                summary: "Failed to remove reaction from post"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not remove reaction from post"
    """

    results, error = PostReactionService(get_jwt_identity()).remove_reaction(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("/comments/<comment_public_id>/reactions", methods=["POST"])
@jwt_required()
@active_status_required
def react_to_comment(comment_public_id):
    """
    React to Comment Endpoint
    This allows users to react to a comment
    ---
    tags:
      - Reaction
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ReactionRequest'
    responses:
      200:
        description: Reaction changed Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Changed to liked"
                    data:
                      type: object
      201:
        description: Reaction created Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Comment liked"
                    data:
                      type: object
      400:
        description: Bad Request
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BadRequestErrorResponse'
            examples:
              invalid_reaction_type:
                summary: "Invalid reaction type"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Invalid reaction type must be either (like) or (dislike)"
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
              not_found:
                summary: "The comment does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Comment not found"
      409:
        description: Conflict Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              already_exists:
                summary: "Already have that reaction to a particular comment"
                value:
                  success: false
                  error: "Conflict Error"
                  message: "Comment already liked"
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
                    reaction_type: 
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
            examples:
              request_failed:
                summary: "Failed to react to comment"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not react to comment"
    """
    try:
        data: [dict] = reaction_schema.load(request.get_json(silent=True))
        pass
    except ValidationError as e:
        return api_response.schema_error(e.messages)
    
    results, error = CommentReactionService(get_jwt_identity()).toggle_reaction(comment_public_id,  data.get("reaction_type"))

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("/comments/<comment_public_id>/reactions", methods=["DELETE"])
@jwt_required()
@active_status_required
def remove_comment_reaction(comment_public_id):
    """
    Remove Comment Reaction Endpoint
    This allows users to remove the reaction they made to a comment
    ---
    tags:
      - Reaction
    responses:
      200:
        description: Reaction removed Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Reaction removed"
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
              post_not_found:
                summary: "The comment does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Comment not found"
              reaction_not_found:
                summary: "The reaction does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Reaction not found" 
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
                summary: "Failed to remove reaction from comment"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not remove reaction from comment"
    """
    results, error = CommentReactionService(get_jwt_identity()).remove_reaction(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("/posts/reactions", methods=["GET"])
@jwt_required()
@active_status_required
def get_reacted_posts_public_id_list():
    """
    Get Post Reactions List Endpoint
    This allows a user to get the list of post public ids that they reacted to. This is to be used for rendering state in the frontend 
    ---
    tags:
      - Reaction
    responses:
      200:
        description: Reaction list Sent
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
    results, error = PostReactionService(get_jwt_identity()).get_reacted_posts_public_id_list()
    
    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("comments/reactions", methods=["GET"])
@jwt_required()
@active_status_required
def get_reacted_comments_public_id_list():
    """
    Get Comment Reactions List Endpoint
    This allows a user to get the list of comment public ids that they reacted to. This is to be used for rendering state in the frontend 
    ---
    tags:
      - Reaction
    responses:
      200:
        description: Reaction list Sent
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
    results, error = CommentReactionService(get_jwt_identity()).get_reacted_comments_public_id_list()
    
    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))