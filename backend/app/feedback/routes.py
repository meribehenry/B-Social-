from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.feedback.service import FeedbackService
from app.feedback.schema import NewFeedbackSchema
from app.shared.response import APIResponse


feedbacks_bp = Blueprint("feedbacks", __name__, url_prefix="/api/v1/feedbacks")

api_response = APIResponse()


@feedbacks_bp.route("/", methods=["POST"])
@jwt_required()
def submit_feedback():
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
def delete_feedback(feedback_public_id):
    results, error = FeedbackService(get_jwt_identity()).delete_feedback(feedback_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@feedbacks_bp.route("/", methods=["GET"])
@jwt_required()
def view_feedbacks():
    feedback_next_page = request.args.get("page", 1, type=int)
    results, error = FeedbackService(get_jwt_identity()).view_feedbacks(page=feedback_next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
