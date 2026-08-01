from flask import Blueprint, request
from flask_jwt_extended import  jwt_required 
from marshmallow import ValidationError
from app.search.schema import SearchFieldSchema
from app.search.service import SearchService
from app.shared.response import APIResponse


search_bp = Blueprint("search", __name__, url_prefix="/api/v1/search")

api_response = APIResponse()


@search_bp.route("/", methods=["GET"])
@jwt_required()
def global_search():
    next_page = request.args.get("page", 1, type=int)
    try:
        data: [dict] = SearchFieldSchema().load({"search_term": request.args.get("search", "", type=str)})
        print(data)
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = SearchService().global_search(data, page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))