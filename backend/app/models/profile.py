from app.extensions import db
import uuid6


class Profile(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_pic_url = db.Column(db.String(255), default="default.jpg", nullable=False)
    profile_pic_id = db.Column(db.String(100), default="default", nullable=False)
    num_of_posts = db.Column(db.Integer, default=0, nullable=False)
    num_of_followers = db.Column(db.Integer, default=0, nullable=False)
    num_of_following = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)