from datetime import datetime, timezone
from app.extensions import db
import uuid6


class Report(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    case_id = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    
