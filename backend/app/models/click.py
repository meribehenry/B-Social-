from app.extensions import db
import uuid6


class Click(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    viewed= db.Column(db.Boolean, default=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String(20), nullable=False)