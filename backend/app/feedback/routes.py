from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.feedback.service import FeedbackService
from app.feedback.schema import NewFeedbackSchema
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required, admin_required


feedbacks_bp = Blueprint("feedbacks", __name__, url_prefix="/api/v1/feedbacks")

api_response = APIResponse()


@feedbacks_bp.route("/", methods=["POST"])
@jwt_required()
@active_status_required
def submit_feedback():
    """
    New Feedback Endpoint
    This allows users to give feedback
    ---
    tags:
      - Feedback
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/FeedbackRequest'
    responses:
      201:
        description: Feedback submitted Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Feedback submitted Successfully"
                    data:
                      $ref: '#/components/schemas/FeedbackResponseSchema'
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
                summary: "Failed to submit feedback"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not submit feedback"
    """
    try:
        data: [dict] = NewFeedbackSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = FeedbackService(get_jwt_identity()).submit_feedback(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@feedbacks_bp.route("/<feedback_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
@admin_required
def delete_feedback(feedback_public_id):
    """
    Delete Feedback Endpoint
    This allows admin to delete feedback
    ---
    tags:
      - Feedback
    responses:
      200:
        description: Feedback deleted Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Feedback deleted Successfully"
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
                summary: "The feedback does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Feedback not found"
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
    results, error = FeedbackService(get_jwt_identity()).delete_feedback(feedback_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@feedbacks_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
@admin_required
def view_feedbacks():
    """
    View Feedbacks Endpoint
    This allows admin to view all feedbacks
    ---
    tags:
      - Feedback
    responses:
      200:
        description: Feedback Sent
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
                        feedbacks:
                          type: array
                          items:
                            $ref: '#/components/schemas/FeedbackResponseSchema'
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
    feedback_next_page = request.args.get("page", 1, type=int)
    results, error = FeedbackService(get_jwt_identity()).view_feedbacks(page=feedback_next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
