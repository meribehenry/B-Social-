from flask import Blueprint, request
from app.reaction.schema import ReactionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from app.reaction.service import PostReactionService, CommentReactionService
from app.shared.response import APIResponse


reactions_bp = Blueprint("reactions", __name__, url_prefix="/api/v1/")

api_response = APIResponse()
reaction_schema = ReactionSchema()


@reactions_bp.route("/posts/<post_public_id>/reactions", methods=["POST"])
@jwt_required()
def react_to_post(post_public_id):
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
def remove_post_reaction(post_public_id):
    results, error = PostReactionService(get_jwt_identity()).remove_reaction(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reactions_bp.route("/comments/<comment_public_id>/reactions", methods=["POST"])
@jwt_required()
def react_to_comment(comment_public_id):
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
def remove_comment_reaction(comment_public_id):
    results, error = CommentReactionService(get_jwt_identity()).remove_reaction(comment_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))