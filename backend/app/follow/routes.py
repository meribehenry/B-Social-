from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.follow.service import FollowerService
from app.shared.response import APIResponse


follow_bp = Blueprint("follow", __name__, url_prefix="/api/v1/")

api_response = APIResponse()


@follow_bp.route("/users/<user_public_id>/follow", methods=["POST"])
@jwt_required()
def follow(user_public_id):
    
    results, error = FollowerService(get_jwt_identity()).follow_user(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/follow", methods=["DELETE"])
@jwt_required()
def unfollow(user_public_id):
    
    results, error = FollowerService(get_jwt_identity()).unfollow_user(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/followers", methods=["GET"])
@jwt_required()
def view_followers(user_public_id):

    results, error = FollowerService(get_jwt_identity()).get_followers_or_followings(user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@follow_bp.route("/users/<user_public_id>/following", methods=["GET"])
@jwt_required()
def view_following(user_public_id):

    results, error = FollowerService(get_jwt_identity()).get_followers_or_followings(user_public_id, get_type="following")

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))