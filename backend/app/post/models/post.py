from datetime import datetime, timezone
from app.extensions import db
import uuid
import uuid6


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content = db.Column(db.Text, nullable=True)
    type = db.Column(db.String(20), nullable=False)
    media_url = db.Column(db.String(255), nullable=True)
    media_id = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    date_updated = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=True)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_clicks = db.Column(db.Integer, default=0, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_dislikes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    author = db.relationship("User", back_populates="posts")
    comments = db.relationship("Comment", back_populates="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    reactions = db.relationship("PostReaction", back_populates="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    clicks = db.relationship("Click", back_populates="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    