from datetime import datetime, timezone
import cloudinary
import os
from config import Production, Development
from flask import Flask
from app.extensions import db, migrate, bcrypt, login_manager, mail
from app.extensions import scheduler

config_classes = {
    'production': Production,
    'development': Development,
    'default': Development
}

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "default")
        print(os.environ.get("FLASK_CONFIG"))

    app = Flask(__name__)
    print(config_name)
    app.config.from_object(config_classes.get(config_name))


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login in to access this page"
    login_manager.login_message_category = "danger"


    from .models import User
    @login_manager.user_loader
    def load_user(alternative_id):
        return User.query.filter_by(alternative_id=alternative_id).first()
    
    from app.models import OTP
    @scheduler.task('interval', id='delete_expired_otps', seconds=600, misfire_grace_time=900)
    def delete_expired_otps():
        with app.app_context():
            current_time = datetime.now(timezone.utc)
            expired_otps = OTP.query.filter(OTP.expire_time < current_time).delete()
            db.session.commit()
            print(f"Deleted {expired_otps} expired OTPs at {current_time}")
    
    @scheduler.task('interval', id='delete_unverified_user', seconds=900, misfire_grace_time=900)
    def delete_unverified_user():
        with app.app_context():
            current_time = datetime.now(timezone.utc)
            unverified_user = User.query.filter(User.is_verified == False).delete()
            db.session.commit()
            print(f"Deleted {unverified_user} unverified_users at {current_time}")

    scheduler.init_app(app)
    scheduler.start()

    from app.main.routes import main
    app.register_blueprint(main)
    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")
    from app.posts.routes import posts
    app.register_blueprint(posts, url_prefix="/post")
    from app.comments.routes import comments
    app.register_blueprint(comments, url_prefix="/comment")
    from app.profile.routes import profile
    app.register_blueprint(profile, url_prefix="/profile")
    from app.feedback.route import feedback
    app.register_blueprint(feedback, url_prefix="/feedback")

    from app.utils.template_filters import timeago_filter
    app.template_filter('timeago')(timeago_filter)



    return app