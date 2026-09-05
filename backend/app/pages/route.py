from flask import Blueprint, send_from_directory
import os
from app.extensions import limiter


pages_bp = Blueprint("pages", __name__)

FRONTEND_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../frontend")
)

@limiter.limit("100 per minute")
@pages_bp.get("/")
def landing_page():
    return send_from_directory(
        FRONTEND_DIR, 
        "pages/landing_page.html"
    )

@limiter.limit("100 per minute")
@pages_bp.get("/auth")
def auth_page():
    return send_from_directory(
        FRONTEND_DIR, 
        "pages/auth.html"
    )

@limiter.limit("100 per minute")
@pages_bp.get("/js/<path:filename>")
def javascript(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "js"),
        filename
    )

@limiter.limit("400 per minute")
@pages_bp.get("/css/<path:filename>")
def css(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "css"),
        filename
    )

@limiter.limit("100 per minute")
@pages_bp.get("/svgs/<path:filename>")
def svgs(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "svgs"),
        filename
    )

@limiter.limit("100 per minute")
@pages_bp.get("/images/<path:filename>")
def imges(filename):
    return send_from_directory(
        os.path.join(FRONTEND_DIR, "images"),
        filename
    )

@limiter.limit("100 per minute")
@pages_bp.get("/app")
def app_page():
    return send_from_directory(
        FRONTEND_DIR, 
        "pages/index.html"
    )

@limiter.limit("100 per minute")
@pages_bp.get("/app/<path:path>")
def app_page_with_path(path):
    return send_from_directory(
        FRONTEND_DIR, 
        "pages/index.html"
    )

@limiter.limit("100 per minute")
@pages_bp.get("/templates")
def templates():
    return send_from_directory(
        FRONTEND_DIR, 
        "pages/templates.html"
    )
