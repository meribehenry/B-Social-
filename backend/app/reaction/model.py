from app.extensions import db
import uuid6


class PostReaction(db.Model):
    __tablename__ = "post_reactions"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    reaction_type = db.Column(db.String(20), nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    post = db.relationship("Post", back_populates="reactions")
    user = db.relationship("User", back_populates="post_reactions")


class CommentReaction(db.Model):
    __tablename__ = "comments_reactions"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    reaction_type = db.Column(db.String(20), nullable=False)
    comment_id = db.Column(db.String(36), db.ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    comment = db.relationship("Comment", back_populates="reactions")
    user = db.relationship("User", back_populates="comment_reactions")