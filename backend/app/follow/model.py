from datetime import datetime, timezone
from app.extensions import db
import uuid6

class Follower(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    follower_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    followed_user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    followed_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    follower = db.relationship("User", foreign_keys=[follower_id], overlaps="following,followers", back_populates="following")
    followed_user = db.relationship("User", foreign_keys=[followed_user_id], overlaps="following,followers", back_populates="followers")