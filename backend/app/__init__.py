from datetime import datetime, timezone
import os
from config import Production, Development
from flask import Flask
from app.extensions import db, migrate, bcrypt, ma, jwt
from app.extensions import scheduler

config_classes = {
    'production': Production,
    'development': Development,
    'default': Development
}

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_CONFIG", "default")

    app = Flask(__name__)
    app.config.from_object(config_classes.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
 

    from app.auth.services.auth_token_service import TokenService
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        result = TokenService().check_if_jwt_expired(jti)
        return result 
    
    from app.auth.services.otp_service import OTPService
    @scheduler.task('interval', id='delete_expired_otps', seconds=600, misfire_grace_time=900)
    def delete_expired_otps():
        with app.app_context():
            expired_otps_num = OTPService().delete_expired_otps()
            print(f"Deleted {expired_otps_num if expired_otps_num else 0} expired OTPs at {datetime.now(timezone.utc)}")
    
    from app.user.service import UserService
    @scheduler.task('interval', id='delete_unverified_user', seconds=900, misfire_grace_time=900)
    def delete_unverified_user():
        with app.app_context():
            unverified_user_num = UserService().delete_unverified_users()
            print(f"Deleted {unverified_user_num if unverified_user_num else 0} unverified_users at {datetime.now(timezone.utc)}")


    scheduler.init_app(app)
    scheduler.start()

    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from app.post.routes import posts_bp
    app.register_blueprint(posts_bp)
    from app.comment.routes import comments_bp
    app.register_blueprint(comments_bp)
    from app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)
    from app.feedback.routes import feedbacks_bp
    app.register_blueprint(feedbacks_bp)
    from app.follow.routes import follow_bp
    app.register_blueprint(follow_bp)
    from app.moderator.routes import moderator_bp
    app.register_blueprint(moderator_bp)
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp)
    from app.notification.routes import notifications_bp
    app.register_blueprint(notifications_bp)
    from app.report.routes import reports_bp
    app.register_blueprint(reports_bp)
    from app.reaction.routes import reactions_bp
    app.register_blueprint(reactions_bp)
    from app.search.routes import search_bp
    app.register_blueprint(search_bp)
    from app.errors.error_handlers import global_errors_bp
    app.register_blueprint(global_errors_bp)


    return app