from datetime import datetime, timezone
from app.extensions import db
import uuid6


class Notification(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
