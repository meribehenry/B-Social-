from datetime import datetime, timezone, timedelta
from app.extensions import db
import uuid6


class OTP(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    otp_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    expire_time = db.Column(db.DateTime(timezone=True), default=lambda: (datetime.now(timezone.utc) + timedelta(minutes=10)), nullable=False)