from datetime import datetime, timezone
from app.extensions import db
import uuid6


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    recipient_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    actor_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    recipient = db.relationship("User", foreign_keys=[recipient_id], back_populates="notifications")
    actor = db.relationship("User", foreign_keys=[actor_id], back_populates="sent_notifications")
