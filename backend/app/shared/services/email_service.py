from flask import  render_template, url_for
from app.extensions import logger
from concurrent.futures import ThreadPoolExecutor
import os
import requests


executor = ThreadPoolExecutor(max_workers=20)


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
    
    def _send_async_email(self, header, data):
        try:
            response = requests.post(self.url, headers=header, json=data, timeout=10)
            logger.info(f"Email sent successfully 💯: {response.status_code}")
            
            response.raise_for_status()

        except requests.exceptions.Timeout:
            logger.error("Brevo timed out")

        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Brevo")

        except requests.exceptions.HTTPError:
            logger.error("Brevo HTTP Error")
            # if e.response is not None:
            #     logger.error(f"Response content: {e.response.content}")
            #     logger.error(f"Response status code: {e.response.status_code}")

        except requests.exceptions.RequestException:
            logger.error("Unexpected Brevo error")
                
    
    def send_otp(self, email, otp_code):
        html = render_template("otp_code.html", otp_code=otp_code)
        subject = "OTP Code"

        executor.submit(self._send_async_email,
                        self._get_header(), 
                        self._build_email(subject, email, html)
                    )
        
        logger.info("Otp email is been processed in the background")
    

    def send_request_token(self, token, email):
        html =  render_template("reset_request.html", token=token)
        print(f"http://127.0.0.1:5000/auth?view=reset-password&token={token}")
        subject = "Reset Password"

        executor.submit(self._send_async_email,
                                self._get_header(), 
                                self._build_email(subject, email, html)
                            )
        
        logger.info("Reset token email is being processed in the background")
    
    
    def send_welcome_message(self, email):
        html = render_template("welcome_email.html")
        subject = "Welcome to B-Social"

        executor.submit(self._send_async_email,  
                                self._get_header(), 
                                self._build_email(subject, email, html)
                            )
        
        logger.info("Welcome message email is being processed in the background")