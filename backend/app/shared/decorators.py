from functools import wraps
from flask import current_app
from app.shared.response import APIResponse
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.user.service import UserService

api_response = APIResponse()
user_service = UserService()


def active_status_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = user_service.get_user_object(get_jwt_identity())
        if user.status == "suspended":
            return api_response.error(message="Your account has been suspended", status_code=403)
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = user_service.get_user_object(get_jwt_identity())
        if user.role != "admin":
            return api_response.error(message="Your are not authorized to access this endpoint", status_code=403)
        return func(*args, **kwargs)
    return wrapper

def moderator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = user_service.get_user_object(get_jwt_identity())
        if user.role != "admin" and user.role != "moderator":
            return api_response.error(message="Your are not authorized to access this endpoint", status_code=403)
        return func(*args, **kwargs)
    return wrapper


