from datetime import datetime, timezone
from app.extensions import db
import uuid6

class Follower(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    follower_id = db.Column(db.Integer, nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date_followed = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)