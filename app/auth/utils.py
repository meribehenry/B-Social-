from flask import redirect, url_for

from app.extensions import mail
from flask_mail import Message



def send_email(user):
    token = user.generate_reset_token()

    message = Message("Password Reset Request", sender="noreply@gmail.com", recipients=[user.email], reply_to="mercuryboy109@gmail.com")
    message.body= f"""
Please click the link below to be able to reset your password.
Link: {url_for('auth.reset_password', token=token, _external=True)}
If you didn't request this you can simply ignore it and no changes would be made.
"""
    
    mail.send(message)