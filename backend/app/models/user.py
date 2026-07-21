from datetime import datetime, timezone
from app.extensions import db, bcrypt
import uuid
import uuid6


class User(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    profile = db.relationship("Profile", backref="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    followers = db.relationship("Follower", backref="followed_user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    following = db.relationship("Follower", backref="follower")
    post_reaction = db.relationship("PostReaction", backref="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic") 
    comment_reaction = db.relationship("CommentReaction", backref="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    comments = db.relationship("Comment", backref="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    notifications = db.relationship("Notification", backref="owner", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    clicks = db.relationship("Click", backref="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def set_password(self, subnitted_password):
        """ This method hashes user submitted password and passes the value to the db model attribute password"""
        self.password = bcrypt.generate_password_hash(subnitted_password)

    def check_password(self, subnitted_password):
        """This method checks user submitted password against the stored hashed password"""
        return bcrypt.check_password_hash(self.password, subnitted_password)