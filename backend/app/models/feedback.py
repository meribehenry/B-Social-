from datetime import datetime, timezone
from app.extensions import db
import uuid6


class Feedback(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    writer_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)