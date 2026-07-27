from app.models.follower import Follower
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.utils.response import ServiceResponseBuilder


service_response_builder = ServiceResponseBuilder()


class FollowerService():
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first_or_404()
        self.error = {}
        self.result = {}
    
    def follow_user(self, followed_user_public_id):
        followed_user = User.query.filter_by(public_id=followed_user_public_id).first()

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        follower = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first()

        if follower:
            self.error = service_response_builder.conflict_error("Already following user")
            return self.result, self.error
        
        follower = Follower(follower_id=self.current_user.id, followed_user=followed_user) 

        try:
            db.session.add(follower)
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers + 1
            db.session.commit()

        except SQLAlchemyError as e:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers - 1
            db.session.rollback()
            print(f"SQLAlchemy error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        
        except Exception as e:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers - 1
            db.session.rollback()
            print(f"An error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        

        self.result = service_response_builder.result(status_code=201)
        return self.result, self.error 
    
    
    def unfollow_user(self, followed_user_public_id):
        followed_user = User.query.filter_by(public_id=followed_user_public_id).first()

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        follower = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first()

        if not follower:
            self.error = service_response_builder.conflict_error("You are not following user")
            return self.result, self.error
        
        followed_user.profile.num_of_followers = followed_user.profile.num_of_followers - 1

        try:
            db.session.delete(follower)
            db.session.commit()

        except SQLAlchemyError as e:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers + 1
            db.session.rollback()
            print(f"SQLAlchemy error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        except Exception as e:
            followed_user.profile.num_of_followers = followed_user.profile.num_of_followers + 1
            db.session.rollback()
            print(f"An error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        self.result = service_response_builder.result(status_code=201)
        return self.result, self.error 