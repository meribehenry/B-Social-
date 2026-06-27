from functools import wraps
from flask_login import current_user
from flask import redirect, url_for


def verification_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_verified:
            return redirect(url_for("auth.verify_email", user_public_id=current_user.public_id))
        print(current_user.is_verified)
        return func(*args, **kwargs)
    return wrapper