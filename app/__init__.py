from flask import Flask
from app.extensions import db, migrate, bcrypt, login_manager, mail


def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    login_manager.login_message = "Please login in to access this page"
    login_manager.login_message_category = "danger"

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from app.main.routes import main
    app.register_blueprint(main)
    from app.auth.routes import auth
    app.register_blueprint(auth, url_prefix="/auth")

    return app