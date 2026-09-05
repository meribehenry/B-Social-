from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.post.service import PostService
from marshmallow import ValidationError
from app.post.schema import NewPostSchema
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required


posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/posts")

api_response = APIResponse()


@posts_bp.route("", methods=["POST"])
@jwt_required()
@active_status_required
def new_post():
    """
    New Post Endpoint
    This allows users to create a post
    ---
    tags:
      - Post
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/PostRequest'
    responses:
      201:
        description: Post created Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Post created successfully"
                    data:
                      $ref: '#/components/schemas/PostResponseSchema'
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
                summary: "No file or content was sent"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Please enter atleast one field (text or media)"
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
                summary: "Failed to create post"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not create post"
    """
    try:
        data = NewPostSchema().load(request.form)
        file = request.files
    except ValidationError as e:
        print(e)
        return api_response.schema_error(errors=e.messages)
    
    results, error = PostService(get_jwt_identity()).create_post(data, file)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@posts_bp.route("/<post_public_id>", methods=["PATCH"])
@jwt_required()
@active_status_required
def update_post(post_public_id):
    """
    Edit Post Endpoint
    This allows users to edit a post
    ---
    tags:
      - Post
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/PostRequest'
    responses:
      200:
        description: Post updated Successful
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Post updated successfully"
                    data:
                      $ref: '#/components/schemas/PostResponseSchema'
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
                summary: "No file or content was sent"
                value:
                  success: false
                  error: "Bad Request error"
                  message: "Please enter atleast one field (text or media)"
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
                summary: "Unauthorised to edit this post"
                value:
                  success: false
                  error: "Forbidden error"
                  message: "You are not authorized to edit this post"
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
              bad_file_type:
                summary:  When the file sent is not in the allowed extension
                value:
                  success: false
                  message: "Invalid file type. Please enter the correct type: [jpg, img, jpeg, png]"
                  error: "Validation Error"
              deadline_error:
                summary:  Cannot edit post after 48 hours
                value:
                  success: false
                  message: "Cannot edit post after 48 hours"
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
                summary: "Failed to update post"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not update post"
    """
    try:
        data: [dict] = NewPostSchema().load(request.form)
        file = request.files
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = PostService(get_jwt_identity()).edit_post(post_public_id, data, file)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@posts_bp.route("/<post_public_id>", methods=["GET"])
@jwt_required()
@active_status_required
def view_post(post_public_id):
    """
    View Post Endpoint
    This allows users to see a particular post
    ---
    tags:
      - Post
    responses:
      200:
        description: Post Sent
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
                      $ref: '#/components/schemas/PostResponseSchema'
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
                summary: "The Post does not exist"
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
    results, error = PostService(get_jwt_identity()).view_post(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@posts_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
def view_user_posts():
    """
    View Posts Endpoint
    This allows users to see all posts
    ---
    tags:
      - Post
    parameters:
      - name: page
        in: query
        description: The page number to retrieve.
        type: integer
        example: 2
      - name: per_page
        in: query
        type: integer
        description: Number of items per page.
        example: 10
    responses:
      200:
        description: Post Sent
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
                        posts:
                          type: array
                          items:
                            $ref: '#/components/schemas/PostResponseSchema'
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
    posts_next_page = request.args.get("page", 1, type=int)
    posts_per_page = request.args.get("per_page", 20, type=int)
    user_public_id = request.args.get("user_public_id")
    results, error = PostService(get_jwt_identity()).view_posts(page=posts_next_page, per_page=posts_per_page, user_public_id=user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@posts_bp.route("/<post_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
def delete_post(post_public_id):
    """
    Delete Post Endpoint
    This allows users to delete a particular post
    ---
    tags:
      - Post
    responses:
      200:
        description: Post Deleted
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Post successfully deleted"
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
              already_exists:
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
    results, error = PostService(get_jwt_identity()).delete_post(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))