from app.extensions import db
import uuid6


class TokenBlocklist(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    jti = db.Column(db.String(30), nullable=False)
