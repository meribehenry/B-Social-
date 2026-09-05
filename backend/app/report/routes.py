from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.report.service import ReportService
from marshmallow import ValidationError
from app.report.schema import NewReportSchema
from app.shared.response import APIResponse
from app.shared.decorators import active_status_required, moderator_required, admin_required


reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/reports")

api_response = APIResponse()


@reports_bp.route("/", methods=["POST"])
@jwt_required()
@active_status_required
def new_report():
    """
    New Report Endpoint
    This allows users to make a report
    ---
    tags:
      - Report
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ReportRequest'
    responses:
      201:
        description: Report created Successfully
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Report created successfully"
                    data:
                      $ref: '#/components/schemas/ReportResponseSchema'
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
      404:
        description: Not Found Error
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ErrorResponse'
            examples:
              not_found:
                summary: "The reported *case type* does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "The reported post does not exist"
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
              report_error:
                summary:  When user trys to report themselves
                value:
                  success: false
                  message: "Input validation failed"
                  error: "Validation Error"
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
                summary: "Failed to create report"
                value:
                  success: false
                  error: "Internal Server Error"
                  message: "Could not create report"
    """
    try:
        data: [dict] = NewReportSchema().load(request.get_json())
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = ReportService(get_jwt_identity()).create_report(data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@reports_bp.route("/<report_public_id>", methods=["GET"])
@jwt_required()
@active_status_required
@moderator_required
def view_report(report_public_id):
    """
    View Report Endpoint
    This allows moderators and admins to see a particular report
    ---
    tags:
      - Report
    responses:
      200:
        description: Report Sent
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
                      $ref: '#/components/schemas/ReportResponseSchema'
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
              not_found:
                summary: "The report does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Report not found"
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

    results, error = ReportService(get_jwt_identity()).view_report(report_public_id)
    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reports_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
@moderator_required
def view_reports():
    """
    View Reports Endpoint
    This allows moderator and admins to see all the reports
    ---
    tags:
      - Report
    responses:
      200:
        description: Reports Sent
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
                        reports:
                          type: array
                          items:
                            $ref: '#/components/schemas/ReportResponseSchema'
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
    results, error = ReportService(get_jwt_identity()).view_reports(page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reports_bp.route("/<report_public_id>", methods=["DELETE"])
@jwt_required()
@active_status_required
@admin_required
def delete_report(report_public_id):
    """
    View Report Endpoint
    This allows moderators or admins to delete a particular report
    ---
    tags:
      - Report
    responses:
      200:
        description: Report Sent
        content:
          application/json:
            schema:
              allOf:
                - $ref: '#/components/schemas/SuccessResponse'
                - type: object
                  properties:
                    message: 
                      type: string
                      example: "Report deleted successfully"
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
              not_found:
                summary: "The report does not exist"
                value:
                  success: false
                  error: "Not found error"
                  message: "Report not found"
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
    results, error = ReportService(get_jwt_identity()).delete_report(report_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))