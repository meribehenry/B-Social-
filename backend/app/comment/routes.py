from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.comment.service import CommentService
from marshmallow import ValidationError
from app.shared.response import APIResponse
from app.comment.schema import NewCommentSchema


comments_bp = Blueprint("comments", __name__, url_prefix="/api/v1/")

api_response = APIResponse()


@comments_bp.route("/posts/<post_public_id>/comments", methods=["POST"])
@jwt_required()
def new_comment(post_public_id):
    try:
        data = NewCommentSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = CommentService(get_jwt_identity()).create_comment(post_public_id, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/comments/<comment_public_id>", methods=["PATCH"])
@jwt_required()
def edit_comment(comment_public_id):
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
def view_comment(comment_public_id):
    results, error = CommentService(get_jwt_identity()).view_comment(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/posts/<post_public_id>/comments", methods=["GET"])
@jwt_required()
def view_comments(post_public_id):
    comment_next_page = request.args.get("page", 1, type=int)
    results, error = CommentService(get_jwt_identity()).view_comments(post_public_id, page=comment_next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@comments_bp.route("/comments/<comment_public_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_public_id):
    results, error = CommentService(get_jwt_identity()).delete_comment(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))