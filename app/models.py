from datetime import datetime

from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    num_of_posts = db.Column(db.Integer, default=0, nullable=False)
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comments", backref="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")


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




