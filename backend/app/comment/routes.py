from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.comment.service import CommentService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.comment.schema import NewCommentSchema
from app.shared.decorators import active_status_required

comments_bp = Blueprint("comments", __name__, url_prefix="/api/v1")

api_response = APIResponse()


@comments_bp.route("/posts/<post_public_id>/comments", methods=["POST"])
@jwt_required()
@active_status_required
def new_comment(post_public_id):
    """
    New Comment Endpoint
    This allows users to comment on a post
    ---
    tags:
      - Comment
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CommentRequest'
    responses:
      201:
        description: Comment created Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Comment created successfully"
                    data:
                      $ref: '#/components/schemas/CommentResponseSchema'
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
                    content: 
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
                summary: "Failed to create comment"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not create comment"
    """
    try:
        print(request.get_json())
        print(type(request.get_json()))
        data = NewCommentSchema().load(request.get_json())
    except ValidationError as e:
        print(e)
        return api_response.schema_error(errors=e.messages)
    
    results, error = CommentService(get_jwt_identity()).create_comment(post_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/comments/<comment_public_id>", methods=["PATCH"])
@jwt_required()
@active_status_required
def edit_comment(comment_public_id):
    """
    Edit Comment Endpoint
    This allows an users to edit their comment they made under a post
    ---
    tags:
      - Comment
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CommentRequest'
    responses:
      200:
        description: Comment update Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Comment created successfully"
                    data:
                      $ref: '#/components/schemas/CommentResponseSchema'
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
                summary: "Unauthorised to edit this comment"
                value:
                  success: false
                  error: "Forbidden error"
                  message: "You are not authorized to edit this comment"
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
                    content: 
                      - "Field must not be empty"
              deadline_error:
                summary:  Cannot update comment after 48 hours
                value:
                  success: false
                  message: "Cannot update comment after 48 hours"
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
                summary: "Failed to update comment"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not update comment"
    """
    try:
        data = NewCommentSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = CommentService(get_jwt_identity()).edit_comment(comment_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@comments_bp.route("/comments/<comment_public_id>", methods=["GET"])
@jwt_required()
@active_status_required
def view_comment(comment_public_id):
    """
    View Comment Endpoint
    This allows users to see a particular comment
    ---
    tags:
      - Comment
    responses:
      200:
        description: Comment Sent
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
                      $ref: '#/components/schemas/CommentResponseSchema'
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
    results, error = CommentService(get_jwt_identity()).view_comment(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/posts/<post_public_id>/comments", methods=["GET"])
@jwt_required()
@active_status_required
def view_comments(post_public_id):
    """
    View Comments Endpoint
    This allows an users view all the comments on a particular post
    ---
    tags:
      - Comment
    responses:
      200:
        description: Comments Sent
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
                      properties:
                        pagination:
                          $ref: '#/components/schemas/PaginationSchema'
                        comments:
                          type: array
                          items:
                            $ref: '#/components/schemas/CommentResponseSchema'
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
    comment_next_page = request.args.get("page", 1, type=int)
    results, error = CommentService(get_jwt_identity()).view_comments(post_public_id, page=comment_next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/comments/<comment_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
def delete_comment(comment_public_id):
    """
    Delete Comment Endpoint
    This allows users to delete a particular comment
    ---
    tags:
      - Comment
    responses:
      200:
        description: Comment Deleted
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Comment successfully deleted"
                    data:
                      type: object
      401:
        description: Unauthenticated Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              forbidden_error:
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
    results, error = CommentService(get_jwt_identity()).delete_comment(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))