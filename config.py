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
    CLOUDINARY_CLOUD_NAME=os.environ.get("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.environ.get("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.environ.get("CLOUDINARY_API_SECRET")