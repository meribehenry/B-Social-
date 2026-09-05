from flask import Blueprint, request
from flask_jwt_extended import  jwt_required 
from marshmallow import ValidationError
from app.search.schema import SearchFieldSchema
from app.search.service import SearchService
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required


search_bp = Blueprint("search", __name__, url_prefix="/api/v1/search")

api_response = APIResponse()


@search_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
def global_search():
    """
    Search Endpoint
    This allows users to search for posts and other users in the platform
    ---
    tags:
      - Search
    parameters:
      - name: search
        in: query
        type: string
        description: Search keyword for filtering posts.
        example: "python"
    responses:
      200:
        description: Search Result Sent
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
                        users:
                          type: array
                          items:
                            $ref: '#/components/schemas/SearchResponseSchema'
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
    try:
        data: [dict] = SearchFieldSchema().load({"search_term": request.args.get("search", "", type=str)})
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)

    results, error = SearchService().global_search(data, page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))