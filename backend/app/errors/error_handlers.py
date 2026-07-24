from flask import Blueprint, render_template, jsonify
from app.extensions import db

global_errors_bp = Blueprint("global_errors", __name__)


@global_errors_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": "Bad Request", "message": str(error) }), 400

@global_errors_bp.app_errorhandler(403)
def forbidden(error):
    return jsonify({"success": False, "error":"Forbidden", "message": "You are not authorized to access this endpoint"}), 403

@global_errors_bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Not Found", "message": "The resource request does not exist"}), 404


@global_errors_bp.app_errorhandler(422)
def validation_error(error):
    return jsonify({"success": False, "error": "Validation error", "message": str(error) }), 422


@global_errors_bp.app_errorhandler(429)
def too_many_request(error):
    return jsonify({"success": False, "error": "Too many request", "message": str(error) }), 429

@global_errors_bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return jsonify({"success": False, "error":"Internal server error", "message": "Something went wrong. Please try again"}), 500