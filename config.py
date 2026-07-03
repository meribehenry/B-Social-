from datetime import timedelta
import cloudinary
import os

class Config:
    FLASK_APP=os.environ.get("FLASK_APP")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///app.db")
    MAX_CONTENT_LENGTH=5242880
    MAIL_SERVER=os.environ.get("MAIL_SERVER")
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD=os.environ.get("MAIL_PASSWORD")

    cloudinary.config(
    cloud_name = os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key = os.environ.get("CLOUDINARY_API_KEY"),
    api_secret = os.environ.get("CLOUDINARY_API_SECRET"),
    secure = True
)
    
class Development(Config):
	DEBUG=True
	

class Production(Config):
	SESSION_COOKIE_HTTPONLY=True
	SESSION_COOKIE_SECURE=True
	SESSION_COOKIE_SAMESITE='lax'
	PERMANENT_SESSION_LIFETIME=timedelta(days=30)
	REMEMBER_COOKIE_DURATION=timedelta(days=90)
	REMEMBER_COOKIE_HTTPONLY=True
	REMEMBER_COOKIE_SECURE=True
	REMEMBER_COOKIE_SAMESITE='lax'
