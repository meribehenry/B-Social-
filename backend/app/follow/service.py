from app.shared.pagination import create_pagination_dict
from app.follow.model import Follower
from app.user.service import UserService
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.shared.response import ServiceResponseBuilder
from app.notification.service import NotificationService
from app.follow.schema import FollowersResponseSchema2


service_response_builder = ServiceResponseBuilder()
user_service = UserService()


class FollowerService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def follow_user(self, followed_user_public_id):
        followed_user = user_service.get_user_object(followed_user_public_id)

        if followed_user_public_id == self.current_user.public_id:
            self.error = service_response_builder.conflict_error(message="Cannot follow yourself")
            return self.result, self.error

        if not followed_user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        already_followed = Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first() is not None

        if already_followed:
            self.error = service_response_builder.conflict_error("Already following user")
            return self.result, self.error 

        try:
            # self.current_user.following.append(followed_user)
            new_follower = Follower(follower_id=self.current_user.id, followed_user_id=followed_user.id)
            db.session.add(new_follower)
            db.session.commit()
            user_service.update_count(followed_user, type_of_count="follower")

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not follow user")
            return self.result, self.error 
        
        NotificationService(self.current_user.public_id).create_notification(
                    followed_user,
                    content=f"{self.current_user.username} followed you",
                    notification_type="follow"
                )

        self.result = service_response_builder.result(status_code=201)
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
            print("about to remove")
            # self.current_user.following.remove(followed_user)
            db.session.delete(Follower.query.filter_by(followed_user_id=followed_user.id, follower_id=self.current_user.id).first())
            print("removed")
            db.session.commit()
            user_service.update_count(followed_user, type_of_count="follower", increment=False)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at follower_service, follow_user\n{e}")
            self.error = service_response_builder.internal_server_error("Could not unfollow user")
            return self.result, self.error 
        
        self.result = service_response_builder.result(status_code=201)
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
            "followers": FollowersResponseSchema2(many=True).dump(pagination.items),
            "pagination": create_pagination_dict(pagination)
        }

        self.result = service_response_builder.result(data=data, status_code=200)
        return self.result, self.error 