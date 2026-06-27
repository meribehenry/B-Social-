from flask import Flask
from app.extensions import db, migrate, bcrypt, login_manager, mail


def create_app(Config="config.Config"):
    app = Flask(__name__)
    app.config.from_object(Config)


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

    return app