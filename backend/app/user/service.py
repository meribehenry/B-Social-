from app.user.model import User
from app.profile.model import Profile
from app.extensions import db, logger
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
            logger.error("Failed to create new user")
            return False
        
        except Exception as e:
            db.session.rollback()
            logger.error("Failed to create new user")
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

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to delete new user")

    
    def mark_user_email_has_verified(self, identifier, retrival_method="public_id"):
        user = self._retrieve_user(identifier, retrival_method)
        
        try:
            user.is_verified = True
            db.session.commit() 

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to mark user email has verified")
    
    def change_user_password(self, new_hashed_password, identifier, retrival_method="public_id"):
        user = self._retrieve_user(identifier, retrival_method=retrival_method)
        user.password = new_hashed_password

        try:
            db.session.commit()
            logger.info(f"User ({user.username}) changed their password")
            return True

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Failed to change user password")
            return False
        
        except Exception as e:
            db.session.rollback()
            logger.error("Failed to change user password")
            return False

    def update_count(self, app, user_public_id, type_of_count="post", increment=True):
        with app.app_context():
            user = self.get_user_object(user_public_id)
            if not user:
                return False
            
            try:
                if type_of_count == "post":
                    db.session.execute(
                        update(User)
                        .where(User.id==user.id)
                        .values(num_of_posts=(User.num_of_posts + 1) if increment else (User.num_of_posts - 1))
                        )
                
                elif type_of_count == "follower":
                    print("POp")
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
                logger.info(f"User ({user.username}) {type_of_count} count updated")
                return True
            
            except SQLAlchemyError:
                db.session.rollback()
                logger.error(f"Failed to update user {type_of_count} count")
            return False


    def update_user_status(self, user, status):

        try:
            user.status = status
            db.session.commit()
            logger.info(f"User ({user.username}) status changed")
            return True

        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to change user ({user.username}) status ")
        
        return True
    
    def update_user_role(self, user_public_id, role):
        user = self.get_user_object(user_public_id)
        if not user: return None
        
        try:
            user.role = role
            db.session.commit()
            logger.info(f"User ({user.username}) role changed")
            return True

        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to change user ({user.username}) role ")
        
        return True
    
    def delete_unverified_users(self, seconds=900):
        cutoff_time = datetime.now(timezone.utc) - timedelta(seconds=seconds)
        unverified_user_num = User.query.filter(User.is_verified == False, User.date_joined < cutoff_time).delete()

        try:
            db.session.commit()
            return unverified_user_num

        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to delete unverified users")

    @staticmethod
    def get_db_model():
        return User