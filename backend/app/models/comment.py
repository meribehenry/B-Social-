from datetime import datetime, timezone
from app.extensions import db
import uuid
import uuid6


class Comment(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=True)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_dislikes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    reactions = db.relationship("CommentReaction", backref="comment", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
