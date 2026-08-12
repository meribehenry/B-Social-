from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_limiter.util import get_remote_address


def rate_limit_by_user():
    try:
        verify_jwt_in_request(optional=True)
        user_public_id = get_jwt_identity()
        if user_public_id:
            return f"{user_public_id}"
    except Exception:
        pass

    return get_remote_address()
