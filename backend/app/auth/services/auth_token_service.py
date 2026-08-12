from flask import current_app
from app.extensions import db, logger
from sqlalchemy.exc import SQLAlchemyError
from app.user.service import UserService
from app.auth.models.token_blocklist import TokenBlocklist
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, BadSignature, SignatureExpired


user_service = UserService()


class TokenService():

    def generate_reset_token(self, email):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        hash_password = user_service.get_user_object(email, retrival_method="email").password
        return s.dumps({"email":email, "hash_password":hash_password})
    
    
    def verify_reset_token(self, token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token, max_age=max_age)
        except (BadSignature, BadTimeSignature, SignatureExpired):
            return None
        
        user = user_service.get_user_object(data["email"], retrival_method="email")
        if user.password != data["hash_password"]:
            return None
        
        return user
    
    
    def block_jwt_token(self, access_token_jti=None, refresh_token_jti=None):
        try:
            if access_token_jti and refresh_token_jti:
                blocked_access_token = TokenBlocklist(jti=access_token_jti, type="access")
                blocked_refresh_token = TokenBlocklist(jti=refresh_token_jti, type="refresh")
                db.session.add(blocked_access_token)
                db.session.add(blocked_refresh_token)

            elif access_token_jti and not refresh_token_jti:
                blocked_access_token = TokenBlocklist(jti=access_token_jti, type="access")
                db.session.add(blocked_access_token)

            else:
                blocked_refresh_token = TokenBlocklist(jti=refresh_token_jti, type="refresh")   
                db.session.add(blocked_refresh_token)    

            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error("Failed to block jwt token")
            return False
        
        except Exception as e:
            db.session.rollback()
            logger.error("Failed to block jwt token")
            return False
    
    def check_if_jwt_expired(self, jti):
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    def delete_expired_jwt_tokens(self, type="access"):
        if type not in {"access", "refresh"}:
            raise ValueError("Invalid type only (access or refresh) can be used")

        result = TokenBlocklist.query.filter_by(type=type).delete()
        try:
            db.session.commit()
            return result

        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to delete expired {type} tokens")




