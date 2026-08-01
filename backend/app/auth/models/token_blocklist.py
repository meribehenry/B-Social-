from datetime import datetime, timezone
from app.extensions import db
import uuid6


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklists"
    
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    jti = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
