from app.user.model import User
from app.profile.model import Profile
from app.extensions import db
from app.shared.response import ServiceResponseBuilder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import  update
from datetime import datetime, timezone, timedelta

service_response_builder = ServiceResponseBuilder()


class UserService():

    def _retrieve_user(self, identifier, retrival_method):
        if retrival_method == "email":
            user = User.query.filter_by(email=identifier).first()

        elif retrival_method == "username":
            user = User.query.filter_by(username=identifier).first()

        elif retrival_method == "public_id":
            user = User.query.filter_by(public_id=identifier).first()
        else:
            raise Exception ("Invalid retrival method or identifier could not retrieve user")
        
        return user

    def get_user_object(self, identifier, retrival_method="public_id", return_bool=False):
        """ 
        This funtion helps retrive user object for other services to use. Retrival methods includes: email, username and public_id. 
        Identifer refers to what you are using to retrive user. Return Boolean if you don't want the whole user object instead you are checking if user exists.
        """

        user = self._retrieve_user(identifier, retrival_method)

        if not return_bool:
            return user
        
        return user is not None
    
    def create_new_user(self, email, hashed_password, username, firstname, lastname, gender, is_verified=False):
        """ This function creates new user with their corresponding profile. It returns the user object  if user create and false if not """
        user = User(username=username, email=email, password=hashed_password, is_verified=is_verified, gender=gender)
        profile = Profile(firstname=firstname, lastname=lastname, user=user)

        try:
            db.session.add(user)
            db.session.add(profile)
            db.session.commit()
            return user

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service create_new_user\n{e}")
            return False
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at user_service create_new_user\n{e}")
            return False
    
    def delete_user(self, identifier, retrival_method="public_id"):
        """ 
        This funtion delete a user from the database. Retrival methods includes: email, username and public_id. 
        Identifer refers to what you are using to retrive user. It returns a boolean.
        """

        user = self._retrieve_user(identifier, retrival_method)
        
        try:
            db.session.delete(user)
            db.session.commit() 

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service delete_user\n{e}")

        return True if user else False
    
    def mark_user_email_has_verified(self, identifier, retrival_method="public_id"):
        user = self._retrieve_user(identifier, retrival_method)
        
        try:
            user.is_verified = True
            db.session.commit() 

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service mark_user_email_has_verified\n{e}")
    
    def change_user_password(self, new_hashed_password, identifier, retrival_method="public_id"):
        user = self._retrieve_user(identifier, retrival_method)
        user.password = new_hashed_password

        try:
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service change_user_password\n{e}")
            return False
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at user_service change_user_password\n{e}")
            return False
    

    def update_count(self, user, type_of_count="post", increment=True):
        
        try:
            if type_of_count == "post":
                db.session.execute(
                    update(User)
                    .where(User.id==user.id)
                    .values(num_of_posts=(User.num_of_posts + 1) if increment else (User.num_of_posts - 1))
                    )
            
            elif type_of_count == "follower":
                db.session.execute(
                    update(User)
                    .where(User.id==user.id)
                    .values(num_of_followers=(User.num_of_followers + 1) if increment else (User.num_of_followers - 1))
                    )

            elif type_of_count == "following":
                db.session.execute(
                    update(User)
                    .where(User.id==user.id)
                    .values(num_of_following=(User.num_of_following + 1) if increment else (User.num_of_following - 1))
                    )
            else:
                raise Exception ("Invalid type_of_count")
            
            db.session.commit()
            return True
        
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service update_count\n{e}")
            return False
    
    def update_user_status(self, user, status):

        try:
            user.status = status
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service update_user_status\n{e}")
        
        return True
    
    def update_user_role(self, user, role):
        try:
            user.role = role
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service update_user_role\n{e}")
        
        return True
    
    def delete_unverified_users(self, seconds=900):
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=seconds)
        unverified_user_num = User.query.filter(User.is_verified == False, User.date_joined < cutoff_time).delete()

        try:
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at user_service delete_unverified_users\n{e}")
        
        return unverified_user_num
    