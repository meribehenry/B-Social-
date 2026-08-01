from flask import current_app, render_template
from threading import Thread
from flask import current_app
import os
import requests




class EmailService():
    def __init__(self):
        self.url = "https://api.brevo.com/v3/smtp/email"
        self.api_key = os.environ.get("BREVO_API_KEY")
    
    def _get_header(self):
        return {
            "accept": "application/json",
            "api-key": self.api_key,
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
            "htmlContent": html
        }
    
    def _send_async_email(self, app, header, data):
        with app.app_context():
            try:
                response = requests.post(self.url, headers=header, json=data, timeout=15)
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
        html = "<h1>Coming...<h1>" #render_template("emails/otp_code.html", otp_code=otp_code)
        subject = "OTP Code"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header(), 
                     self._build_email(subject, email, html))
                     ).start()
        
        print("Otp is been processed in the background")
    

    def send_request_token(self, token, email):
        html =  "<h1>Coming...<h1>" #render_template("emails/reset_request.html", token=token)
        subject = "Reset Password"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header(),  
                     self._build_email(subject, email, html))
                     ).start()
        
        print("Reset token is being processed in the background")
    
    
    def send_welcome_message(self, email):
        html = "<h1>Coming...<h1>" #render_template("emails/welcome_email.html")
        subject = "Welcome to B-Social"

        Thread(target=self._send_async_email, 
               args=(current_app._get_current_object(), 
                     self._get_header(),  
                     self._build_email(subject, email, html))
                     ).start()
        
        print("Welcome message is being processed in the background")