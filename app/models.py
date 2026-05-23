from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from app.extensions import db
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired, BadTimeSignature


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    profile_pic_url = db.Column(db.String(255), default="https://res.cloudinary.com/ddzmfmexs/image/upload/v1779357666/default_bqkr3f.jpg", nullable=False)
    profile_pic_id = db.Column(db.String(100), default="default", nullable=False)
    num_of_posts = db.Column(db.Integer, default=0, nullable=False)
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def generate_reset_token(self):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return s.dumps(f"{'user_id': self.id, 'password_hash': self.passowrd}")    

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

        try:
            data = s.loads(token, max_age=max_age)
            user_id = data["user_id"]
            password_hash = data["password_hash"]
        except (SignatureExpired, BadTimeSignature, BadSignature):
            return None
        
        user = User.query.get(user_id)

        if user.password != password_hash:
            return None
        return user
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    post_type = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    photo_id = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    author = db.relationship("User", backref="comments")
