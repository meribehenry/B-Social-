from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.post.service import PostService
from marshmallow import ValidationError
from app.post.schema import NewPostSchema
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required


posts_bp = Blueprint("posts", __name__, url_prefix="/api/v1/posts")

api_response = APIResponse()


@posts_bp.route("/", methods=["POST"])
@jwt_required()
@active_status_required
def new_post():
    try:
        data: [dict] = NewPostSchema().load(request.form)
        file = request.files
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = PostService(get_jwt_identity()).create_post(data, file)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@posts_bp.route("/<post_public_id>", methods=["PATCH"])
@jwt_required()
@active_status_required
def update_post(post_public_id):
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
    results, error = PostService(get_jwt_identity()).view_post(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@posts_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
def view_user_posts():
    posts_next_page = request.args.get("page", 1, type=int)
    user_public_id = request.args.get("user_public_id")
    results, error = PostService(get_jwt_identity()).view_posts(page=posts_next_page, user_public_id=user_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@posts_bp.route("/<post_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
def delete_post(post_public_id):
    results, error = PostService(get_jwt_identity()).delete_post(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))