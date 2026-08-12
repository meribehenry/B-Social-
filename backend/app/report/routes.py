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
    results, error = ReportService(get_jwt_identity()).view_report(report_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reports_bp.route("/", methods=["GET"])
@jwt_required()
@active_status_required
@moderator_required
def view_reports():
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
    results, error = ReportService(get_jwt_identity()).delete_report(report_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))