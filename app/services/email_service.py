from flask import current_app, render_template
from threading import Thread
from flask import current_app
import requests




class EmailService():
    def __init__(self):
        self.url = "https://api.brevo.com/v3/smtp/email"
        self.api_key = current_app.config.get("BREVO_API_KEY")
    
    def _get_header(self):
        return {
            "accept": "application/json",
            "api_key": self.api_key,
            "content_type": "application/json"
        }

    def _build_email(self, subject, recipient, html):
        return {
            "sender": {
                "name": "B-Social",
                "email": "mercuryboy109@gmail.com"
            },
             
            "to": [
                    {
                        "email": recipient
                    }
                ],
            
            "subject": subject,
            "htmlcontent": html
        }
    
    def _send_async_email(self, app, header, data):
        with app.app_context():
            try:
                response = requests.post("https://api.brevo.com/v3/smtp/email", headers=header, json=data)
                print(f"Email sent successfully 💯: {response.status_code}")
                
                response.raise_for_status()

            except requests.exceptions.Timeout:
                print("Brevo timed out.")
                raise

            except requests.exceptions.ConnectionError:
                print("Cannot connect to Brevo.")
                raise

            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e}")
                if e.response is not None:
                    print(e.response.text)
                raise

            except requests.exceptions.RequestException as e:
                print(f"Unexpected error: {e}")
                raise


    
    def send_otp(self, email, otp_code):
        html = render_template("emails/otp_code.html", otp_code=otp_code)
        subject = "OTP Code"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header, 
                     self._build_email(subject, email, html)), 
                     daemon=True
                     ).start()
        
        print("Otp is been processed in the background")
    

    def send_request_token(self, token, email):
        html = render_template("emails/reset_request.html", token=token)
        subject = "Reset Password"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header,  
                     subject,
                     self._build_email(subject, email, html)), 
                     daemon=True).start()
        
        print("Reset token is being processed in the background")
    
    
    def send_welcome_message(self, email):
        html = render_template("emails/welcome_email.html")
        subject = "Welcome to B-Social"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header,  
                     subject,
                     self._build_email(subject, email, html)), 
                     daemon=True).start()
        
        print("Welcome message is being processed in the background")

















    # self.data["to"] = [
    #     {
    #         "email": self.email
    #     }
    # ]

    # self.data["subject"] = "Reset Token"
    # self.data["textContent"] = f"""
    # Please click the link below to be able to reset your password.
    # Link: {url_for('auth.reset_password', token=token, _external=True)}
    # If you didn't request this you can simply ignore it and no changes would be made.
    # """
    # message = Message("Reset Token", recipients=[self.email], sender=current_app.config['MAIL_DEFAULT_SENDER'])
    # message.body = f"""
    # Please click the link below to be able to reset your password.
    # Link: {url_for('auth.reset_password', token=token, _external=True)}
    # If you didn't request this you can simply ignore it and no changes would be made.
    # """
    # message = Message("OTP Code", recipients=[self.email], sender=current_app.config['MAIL_DEFAULT_SENDER'])
    # message.body = f"""
    # Your otp code has arrived and it expires in ten minutes, use it in time. 
    # If you didn't request this you can simply ignore and no changes would be made.
    # OTP CODE: {otp}
    # """ 
    
    # try:
    #     print("Creating message...")
    #     print(f"Server: {current_app.config['MAIL_SERVER']}")
    #     print(f"Port: {current_app.config['MAIL_PORT']}")
    #     print(f"Username: {current_app.config['MAIL_USERNAME']}")
    #     print("Sending email...")
        
    #     mail.send(message)
    #     print("Email sent successfully...")
    # except Exception as e:
    #     print(f"SMTP Error: {e}")
    #     raise

    # self.data["to"] = [
    #     {
    #         "email": self.email
    #     }
    # ]

    # self.data["subject"] = "OTP CODE"
    # self.data["textContent"] = f"""
    # Your otp code has arrived and it expires in ten minutes, use it in time. 
    # If you didn't request this you can simply ignore and no changes would be made.
    # OTP CODE: {otp}
    # """