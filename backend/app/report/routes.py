from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required 
from app.report.service import ReportService
from marshmallow import ValidationError
from app.report.schema import NewReportSchema
from app.shared.response import APIResponse


reports_bp = Blueprint("reports", __name__, url_prefix="/api/v1/reports")

api_response = APIResponse()


@reports_bp.route("/<case_type>/<reported_case_id>", methods=["POST"])
@jwt_required()
def new_report(case_type, reported_case_id):
    try:
        data: [dict] = NewReportSchema().load(request.form)
        file = request.files
    except ValidationError as e:
        return api_response.schema_error(errors=e.messages)
    
    results, error = ReportService(get_jwt_identity()).create_report(reported_case_id, case_type, data)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))
    

@reports_bp.route("/<reported_case_id>", methods=["GET"])
@jwt_required()
def view_report(reported_case_id):
    results, error = ReportService(get_jwt_identity()).view_report(reported_case_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reports_bp.route("/", methods=["GET"])
@jwt_required()
def view_reports():
    next_page = request.args.get("page", 1, type=int)
    results, error = ReportService(get_jwt_identity()).view_reports(page=next_page)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))


@reports_bp.route("/<reported_case_id>", methods=["DELETE"])
@jwt_required()
def delete_report(post_public_id):
    results, error = ReportService(get_jwt_identity()).delete_report(post_public_id)

    if error:
        return api_response.error(error=error.get("error"), message=error.get("message"), status_code=error.get("status_code"))
    
    return api_response.success(data=results.get("data"), message=results.get("message"), status_code=results.get("status_code"))