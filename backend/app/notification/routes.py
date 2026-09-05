from flask import Blueprint, request, Response, stream_with_context
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.notification.service import NotificationService
from app.shared.decorators import active_status_required
from app.shared.response import APIResponse


notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")

api_response = APIResponse()


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
def view_notifications():
    """
    View Notifications Endpoint
    This allows an users view all their notifications
    ---
    tags:
      - Notification
    responses:
      200:
        description: Notifications Sent
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
                        notifications:
                          type: array
                          items:
                            $ref: '#/components/schemas/NotificationResponseSchema'
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
    next_page = request.args.get("page", 1, type=int)
    results, error = NotificationService(get_jwt_identity()).get_notifications(page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@notifications_bp.route("/<notification_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
def delete_notification(notification_public_id):
    """
    Delete Notification Endpoint
    This allows users to delete a particular notification
    ---
    tags:
      - Notification
    responses:
      200:
        description: Notification Deleted
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Notification successfully deleted"
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
                summary: "The Notification does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Notification not found"
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

    results, error = NotificationService(get_jwt_identity()).delete_notification(notification_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@notifications_bp.route("/", methods=["DELETE"])
@jwt_required()
@active_status_required
def delete_all_notifications():
    """
    Delete Notifications Endpoint
    This allows users to delete all their notifications
    ---
    tags:
      - Notification
    responses:
      200:
        description: Notifications Deleted
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Notifications successfully deleted"
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

    results, error = NotificationService(get_jwt_identity()).delete_all_notifications()

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@notifications_bp.route("/count", methods=["GET"])
@jwt_required()
@active_status_required
def get_notification_count():
    """
    Get Notification Count Endpoint
    This allows users to get their notification count
    ---
    tags:
      - Notification
    responses:
      200:
        description: Notifications Count Sent
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
                        notification_count:
                          type: integer
                          example: 9
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

    results, error = NotificationService(get_jwt_identity()).get_notification_count()

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@notifications_bp.route("/stream", methods=["GET"])
@jwt_required()
@active_status_required
def notification_stream():
    """
    Get Notification Stream Endpoint
    This allows users to get notification as they are been created 
    ---
    tags:
      - Notification
    responses:
      200:
        description: Notification Stream Sent
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
                      $ref: '#/components/schemas/NotificationStreamResponseSchema'
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
    result = NotificationService(get_jwt_identity()).notification_event_stream()

    return Response(stream_with_context(result), mimetype='text/event-stream')