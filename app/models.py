from datetime import datetime, timezone, timedelta
import uuid
from flask_login import UserMixin
from app.extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    alternative_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    followers = db.relationship("Follower", backref="followed_user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    post_reaction = db.relationship("PostReaction", backref="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic") 
    comment_reaction = db.relationship("CommentReaction", backref="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    comments = db.relationship("Comment", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def get_id(self):
        return self.alternative_id
    

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text(300), nullable=True)
    profile_pic_url = db.Column(db.String(255), default="default.jpg", nullable=False)
    profile_pic_id = db.Column(db.String(100), default="default", nullable=False)
    num_of_posts = db.Column(db.Integer, default=0, nullable=False)
    num_of_followers = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content = db.Column(db.Text, nullable=True)
    post_type = db.Column(db.String(20), nullable=False)
    photo_url = db.Column(db.String(255), nullable=True)
    photo_id = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_clicks = db.Column(db.Integer, default=0, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_dislikes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    likes = db.relationship("PostReaction", backref="post", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def is_liked_by(self, current_user):
        return self.likes.query.filter_by(user_id=current_user.id).first().liked is not None
    
    def is_disliked_by(self, current_user):
        return self.likes.query.filter_by(user_id=current_user.id).first().disliked is not None


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    edited = db.Column(db.Boolean, default=False, nullable=False)
    num_of_likes = db.Column(db.Integer, default=0, nullable=False)
    num_of_dislikes = db.Column(db.Integer, default=0, nullable=False)
    num_of_comments = db.Column(db.Integer, default=0, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    likes = db.relationship("CommentReaction", backref="comment", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def is_liked_by(self, current_user):
        return self.likes.query.filter_by(user_id=current_user.id).first().liked is not None
    
    def is_disliked_by(self, current_user):
        return self.likes.query.filter_by(user_id=current_user.id).first().disliked is not None


class PostReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked = db.Column(db.Boolean, default=False, nullable=False)
    disliked = db.Column(db.Boolean, default=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String(20), nullable=False)


class CommentReaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked = db.Column(db.Boolean, default=False, nullable=False)
    disliked = db.Column(db.Boolean, default=False, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String(20), nullable=False)
 

class Clicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewed= db.Column(db.Boolean, default=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"), nullable=False)
    username = db.Column(db.String(20), nullable=False)


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp_code = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    expire_time = db.Column(db.DateTime(timezone=True), default=lambda: (datetime.now(timezone.utc) + timedelta(minutes=10)), nullable=False)


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, nullable=False)
    followed_user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    date_followed = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writer = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    # writer_public_id = db.Column(db.String(50), default="None", nullable=False)
    # writer_username = db.Column(db.String(20), default="None", nullable=False)
