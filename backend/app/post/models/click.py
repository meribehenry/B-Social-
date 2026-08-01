from app.extensions import db
import uuid6


class Click(db.Model):
    __tablename__ = "clicks"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    viewed= db.Column(db.Boolean, default=False, nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    post = db.relationship("Post", back_populates="clicks")
    user = db.relationship("User", back_populates="clicks")