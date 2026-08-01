from datetime import datetime, timezone
from app.extensions import db, bcrypt
import uuid
import uuid6


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), default=lambda: str(uuid6.uuid7()), primary_key=True)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    date_joined = db.Column(db.DateTime(timezone=True), default= lambda: datetime.now(timezone.utc), nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(20), default="user", nullable=False)
    num_of_posts = db.Column(db.Integer, default=0, nullable=False)
    num_of_followers = db.Column(db.Integer, default=0, nullable=False)
    num_of_following = db.Column(db.Integer, default=0, nullable=False)
    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)

    followers = db.relationship("Follower", foreign_keys="[Follower.followed_user_id]", back_populates="followed_user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    following = db.relationship("Follower", foreign_keys="[Follower.follower_id]", back_populates="follower", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    notifications = db.relationship("Notification", back_populates="recipient", foreign_keys="Notification.recipient_id", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    sent_notifications = db.relationship("Notification", back_populates="actor", foreign_keys="Notification.actor_id", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    feedbacks = db.relationship("Feedback", back_populates="writer", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    post_reactions = db.relationship("PostReaction", back_populates="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic") 
    comment_reactions = db.relationship("CommentReaction", back_populates="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    comments = db.relationship("Comment", back_populates="author", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")
    clicks = db.relationship("Click", back_populates="user", cascade="all, delete-orphan", passive_deletes=True, lazy="dynamic")

    def set_password(self, submitted_password):
        """ This method hashes user submitted password and passes the value to the db model attribute password"""
        self.password = bcrypt.generate_password_hash(submitted_password)

    def check_password(self, submitted_password):
        """This method checks user submitted password against the stored hashed password"""
        return bcrypt.check_password_hash(self.password, submitted_password)


    # followers = db.relationship("User", 
    #                             secondary="followers",
    #                             primaryjoin="User.id==Follower.followed_user_id",
    #                             secondaryjoin="User.id==Follower.follower_id",
    #                             backref=db.backref("following", lazy="dynamic"),
    #                             lazy="dynamic"
    #                         )