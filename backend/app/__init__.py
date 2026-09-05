from datetime import datetime, timezone
from config import Production, Development
from flask import Flask
from app.extensions import db, migrate, bcrypt, ma, jwt, limiter, logger, swagger, cors
from app.extensions import scheduler

import os

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

    cors.init_app(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500", "http://127.0.0.1:5501", "file:///C:/Users/PC/Desktop/B-Social/frontend/js/app.js"], #[span_8](start_span)[span_8](end_span)
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"], #[span_9](start_span)[span_9](end_span)
            "allow_headers": ["Content-Type", "Authorization"] #[span_10](start_span)[span_10](end_span)
        }
    }, supports_credentials=True)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    swagger.init_app(app)
    
 

    from app.auth.services.auth_token_service import TokenService
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        result = TokenService().check_if_jwt_expired(jti)
        return result 
    
    from app.auth.services.otp_service import OTPService
    @scheduler.task('interval', id='delete_expired_otps', seconds=600, misfire_grace_time=600)
    def delete_expired_otps():
        with app.app_context():
            expired_otps_num = OTPService().delete_expired_otps()
            logger.info(f"Deleted {expired_otps_num if expired_otps_num else 0} expired OTPs at {datetime.now(timezone.utc)}")

    from app.auth.services.auth_token_service import TokenService
    @scheduler.task('interval', id='delete_expired_access_token', seconds=1200, misfire_grace_time=1200)
    def delete_expired_access_token():
        with app.app_context():
            expired_access_token_num = TokenService().delete_expired_jwt_tokens(type="access")
            if expired_access_token_num:
                logger.info(f"Deleted {expired_access_token_num} expired access token at {datetime.now(timezone.utc)}")

    @scheduler.task('interval', id='delete_expired_refresh_token', seconds=2400, misfire_grace_time=2400)
    def delete_expired_refresh_token():
        with app.app_context():
            expired_refresh_token_num = TokenService().delete_expired_jwt_tokens(type="refresh")
            if expired_refresh_token_num:
                logger.info(f"Deleted {expired_refresh_token_num} expired refresh token at {datetime.now(timezone.utc)}")
    
    from app.user.service import UserService
    @scheduler.task('interval', id='delete_unverified_user', seconds=900, misfire_grace_time=900)
    def delete_unverified_user():
        with app.app_context():
            unverified_user_num = UserService().delete_unverified_users()
            if unverified_user_num:
                logger.info(f"Deleted {unverified_user_num} unverified_users at {datetime.now(timezone.utc)}")


    from app.shared.services.file_service import FileService
    @scheduler.task('interval', id='delete_old_file_from_storage', seconds=3600, misfire_grace_time=3600)
    def delete_old_file_from_storage():
        with app.app_context():
            with open("old_media.txt", "r") as file:
                if file:
                    failed = []
                    for file_id in file:
                        r = FileService().delete_file(file_id.strip())
                        logger.info(f"Deleted file ({file_id.strip()}) in old_media.txt") if r else failed.append(file_id)

                    with open("old_media.txt", "w") as f:
                        f.writelines(failed)


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
    from app.pages.route import pages_bp
    app.register_blueprint(pages_bp)
    from app.user.route import user_bp 
    app.register_blueprint(user_bp)

    return app