from flask import current_app
from app.models import User
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, BadSignature, SignatureExpired

class TokenService():

    def generate_reset_token(self, email):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        hash_password = User.query.filter_by(email=email).first().password
        return s.dumps({"email":email, "hash_password":hash_password})
    
    def verify_reset_token(self, token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token, max_age=max_age)
        except (BadSignature, BadTimeSignature, SignatureExpired):
            return None
        
        user = User.query.filter_by(email=data["email"]).first()
        if user.password != data["hash_password"]:
            return None
        
        return user
