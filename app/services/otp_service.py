from datetime import datetime, timezone, timedelta
from app.extensions import db
from app.models import OTP
from sqlalchemy.exc import SQLAlchemyError
import random 

class OTPService():

    def generate_otp(self, email):
        while True:
            otp_code = random.randint(100000, 999999)
            user_exist = OTP.query.filter_by(email=email).first()

            if not user_exist:
                otp = OTP(otp_code=otp_code, email=email, expire_time=(datetime.now(timezone.utc) + timedelta(minutes=10)))
                try:
                    db.session.add(otp)
                    db.session.commit()
                except SQLAlchemyError:
                    db.session.rollback()
                    return None
                return otp_code
            
            else: 
                db.session.delete(user_exist)
                db.session.commit()

    def verify_otp(self, submitted_otp_code, email):
        recorded_otp = OTP.query.filter_by(email=email).first()
        current_time = datetime.now(timezone.utc)

        recorded_otp.expire_time = recorded_otp.expire_time.replace(tzinfo=timezone.utc)

        if current_time > recorded_otp.expire_time:
            return False
        
        if recorded_otp.otp_code == submitted_otp_code:
            return True