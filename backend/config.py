from datetime import timedelta
import cloudinary
import os

class Config:
    FLASK_APP=os.environ.get("FLASK_APP")
    SECRET_KEY=os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///app.db")
    MAX_CONTENT_LENGTH=int(os.environ.get("MAX_CONTENT_LENGTH", 5242880))
    BREVO_API_KEY=os.environ.get("BREVO_API_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 60)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 30)))


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