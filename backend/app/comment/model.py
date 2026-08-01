from datetime import datetime, timezone
from app.extensions import db
import uuid
import uuid6


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=True)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_dislikes = db.Column(db.Integer, default=0, nullable=False)
    num_of_replies = db.Column(db.Integer, default=0, nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    post = db.relationship("Post", back_populates="comments")
    author = db.relationship("User", back_populates="comments")
    reactions = db.relationship("CommentReaction", back_populates="comment", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
