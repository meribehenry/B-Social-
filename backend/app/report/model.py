from datetime import datetime, timezone
from app.extensions import db
import uuid6
import uuid


class Report(db.Model):
    __tablename__ = "reports"
    
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    type = db.Column(db.String(36), nullable=False)
    case_id = db.Column(db.String(36), nullable=False)
    case = db.Column(db.String(36), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    
