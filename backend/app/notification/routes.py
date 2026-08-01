from flask import Blueprint, request, Response, stream_with_context
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.notification.service import NotificationService
from marshmallow import ValidationError
from app.shared.response import APIResponse


notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")

api_response = APIResponse()


@notifications_bp.route("/", methods=["GET"])
@jwt_required()
def view_notifications():

    next_page = request.args.get("page", 1, type=int)
    results, error = NotificationService(get_jwt_identity()).get_notifications(page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@notifications_bp.route("/<notification_public_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_public_id):

    results, error = NotificationService(get_jwt_identity()).delete_notification(notification_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
        

@notifications_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_all_notifications():

    results, error = NotificationService(get_jwt_identity()).delete_all_notifications()

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@notifications_bp.route("/count", methods=["GET"])
@jwt_required()
def get_notification_count():

    results, error = NotificationService(get_jwt_identity()).get_notification_count()

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@notifications_bp.route("/stream", methods=["GET"])
@jwt_required()
def notification_stream():
    result = NotificationService(get_jwt_identity()).notification_event_stream()

    return Response(stream_with_context(result), mimetype='text/event-stream')