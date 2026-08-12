from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from app.shared.rate_limit import rate_limit_by_user
from app.shared.logger_setup import setup_logger



convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()
migrate = Migrate()
scheduler = APScheduler()
ma = Marshmallow()
jwt = JWTManager()
limiter = Limiter(key_func=rate_limit_by_user, default_limits=["400 per day", "100 per hour"], storage_uri="memory://", retry_after="delta seconds=300")
logger = setup_logger("b_social_app")



@event.listens_for(Engine, "connect")
def set_sqlite_pragms(dbapi_connection, connection_record):
    if db.engine.url.drivername.startswith("sqlite"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


