from app.shared.pagination import create_pagination_dict
from app.follow.model import Follower
from app.user.service import UserService
from app.extensions import db, logger
from sqlalchemy.exc import SQLAlchemyError
from app.shared.response import ServiceResponseBuilder
from app.notification.service import NotificationService
from app.follow.schema import FollowersResponseSchema
from flask import current_app
from concurrent.futures import ThreadPoolExecutor


service_response_builder = ServiceResponseBuilder()
user_service = UserService()
count_executor = ThreadPoolExecutor(max_workers=5)


class FollowerService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def follow_user(self, followed_user_public_id):
        followed_user = user_service.get_user_object(followed_user_public_id)

        if followed_user_public_id == self.current_user.public_id:
            self.error = service_response_builder.validation_error(message="Cannot follow yourself")
            return self.result, self.error

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        already_followed = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first() is not None

        if already_followed:
            self.error = service_response_builder.conflict_error("Already following user")
            return self.result, self.error 

        new_follower = Follower(follower_id=self.current_user.id, followed_user_id=followed_user.id)

        try:
            db.session.add(new_follower)
            db.session.commit()
            app = current_app._get_current_object()
            logger.info(f"User {self.current_user.username} followed user {followed_user.username}")
            count_executor.submit(user_service.update_count, app, followed_user.public_id, type_of_count="follower")
            count_executor.submit(user_service.update_count, app, self.current_user.public_id, type_of_count="following")

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Could not follow user")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        
        except Exception:
            db.session.rollback()
            logger.error("Could not follow user")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        
        NotificationService(self.current_user.public_id).create_notification(
                    followed_user,
                    content=f"{self.current_user.username} followed you",
                    notification_type="follow"
                )

        self.result = service_response_builder.result(status_code=201, message="Successfully followed user")
        return self.result, self.error 
    
    
    def unfollow_user(self, followed_user_public_id):
        followed_user = user_service.get_user_object(followed_user_public_id)

        if followed_user_public_id == self.current_user.public_id:
            self.error = service_response_builder.conflict_error(message="Cannot unfollow yourself")
            return self.result, self.error

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        not_following_follower = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first() is not None

        if not not_following_follower:
            self.error = service_response_builder.conflict_error("You are not following user")
            return self.result, self.error

        try:
            db.session.delete(Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first())
            db.session.commit()
            app = current_app._get_current_object()
            logger.info(f"User {self.current_user.username} unfollowed user {followed_user.username}")
            count_executor.submit(user_service.update_count, app, followed_user.public_id, type_of_count="follower", increment=False)
            count_executor.submit(user_service.update_count, app, self.current_user.public_id, type_of_count="following", increment=False)

        except SQLAlchemyError:
            db.session.rollback()
            logger.error("Could not unfollow user")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        except Exception :
            db.session.rollback()
            logger.error("Could not unfollow user")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        self.result = service_response_builder.result(status_code=201, message="Successfully unfollowed user")
        return self.result, self.error 
    

    def get_followers_or_followings(self, followed_user_public_id, per_page=20, page=1, get_type="follower"):
        followed_user = user_service.get_user_object(followed_user_public_id)

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error

        pagination = None
        if get_type == "follower":
            pagination = followed_user.followers.paginate(per_page=per_page, page=page)
        elif get_type == "following":
            pagination = followed_user.following.paginate(per_page=per_page, page=page)
        else:
            raise Exception("Invalid type parameter for get_followers_of_followings method")
            
        data = {
            "followers": FollowersResponseSchema(many=True).dump(pagination.items),
            "pagination": create_pagination_dict(pagination)
        }

        self.result = service_response_builder.result(data=data, status_code=200)
        return self.result, self.error 
    

    def get_following_users_public_id_list(self):
        following_user_public_id_list = [ follower.followed_user.public_id for follower in self.current_user.following]
        
        self.result = service_response_builder.result(data=following_user_public_id_list, status_code=200)
        return self.result, self.error 