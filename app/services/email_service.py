from app.extensions import mail
from flask_mail import Message
from flask import url_for
from app.services.otp_service import OTPService
from app.services.token_service import TokenService

class EmailService():

    def __init__(self, email):
        self.email = email
    
    def send_otp(self):
        otp_service = OTPService()
        otp = otp_service.generate_otp(self.email)

        message = Message("OTP Code", recipients=[self.email], sender="mercuryboy109@gmail.com")
        message.body = f"""
Your otp code has arrived and it expires in ten minutes, use it in time. 
If you didn't request this you can simply ignore and no changes would be made.
OTP CODE: {otp}
"""
        
        mail.send(message)
    

    def send_request_token(self):
        token_service = TokenService()
        token = token_service.generate_reset_token(self.email)

        message = Message("Resquest Token", recipients=[self.email], sender="mercuryboy109@gmail.com")
        message.body = f"""
Please click the link below to be able to reset your password.
Link: {url_for('auth.reset_password', token=token, _external=True)}
If you didn't request this you can simply ignore it and no changes would be made.
"""
        
        mail.send(message)
