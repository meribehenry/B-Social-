from dotenv import load_dotenv
from app.post.service import PostService
from app.comment.service import CommentService
from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from app.notification.service import NotificationService
from app.extensions import logger
import os


load_dotenv()

service_response_builder = ServiceResponseBuilder()
user_service = UserService()

passwords = {os.environ.get("MODERATOR_PASSWORD"), os.environ.get("ADMIN_PASSWORD")}
creator_password = os.environ.get("CREATOR_PASSWORD")


class ModeratorService():

    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def take_down_post(self, post_public_id, data:dict):
        password = data.get("password")

        if password not in passwords:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error

        post = PostService(self.current_user.public_id).get_post_object(post_public_id)
        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error

        if post.author == self.current_user:
            self.error = service_response_builder.validation_error("Cannot take down your post, you are a moderator")
            return self.result, self.error

        if post.author.role == "moderator" and self.current_user.role != "admin":
            self.error = service_response_builder.forbidden_error("Cannot take down the post of your fellow moderator only admin can")
            return self.result, self.error

        if post.author.role == "admin" and self.current_user.role != "admin" and password!=creator_password:
            self.error = service_response_builder.forbidden_error("Cannot take down the post of an admin only creator can")
            return self.result, self.error

        
        post_author = post.author
        _, e = PostService(self.current_user.public_id).delete_post(post_public_id)

        if e:
            logger.error("An error at moderator_service take_down_post")
            self.error = e
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    post_author,
                    content=f"Your post was taken down for violating community rule",
                )

        self.result = service_response_builder.result(message="Post removed and author has been notified")
        return self.result, self.error
    

    def take_down_comment(self, comment_public_id, data:dict):
        password = data.get("password")
        
        if password not in passwords:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        comment = CommentService(self.current_user.public_id).get_comment_object(comment_public_id)
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error

        if comment.author == self.current_user:
            self.error = service_response_builder.validation_error("Cannot take down your comment, you are a moderator")
            return self.result, self.error
        
        if comment.author.role == "moderator" and self.current_user.role != "admin":
            self.error = service_response_builder.forbidden_error("Cannot take down the comment of your fellow moderator only admin can")
            return self.result, self.error

        if comment.author.role == "admin" and self.current_user.role != "admin" and password!=creator_password:
            self.error = service_response_builder.forbidden_error("Cannot take down the comment of an admin only creator can")
            return self.result, self.error

        comment_author = comment.author

        _, e = CommentService(self.current_user.public_id).delete_comment(comment_public_id)

        if e:
            logger.error("An error at moderator_service take_down_comment")
            self.error = e
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    comment_author,
                    content=f"Your comment was taken down for violating community rule",
                )
        
        self.result = service_response_builder.result(message="Comment removed and author has been notified")
        return self.result, self.error
    

    def change_user_status(self, user_to_change_public_id, data:dict):
        password = data.get("password")
        status = data.get("status")

        if status not in {"suspended", "active"}:
            self.error = service_response_builder.validation_error(message="Invalid status type")
            return self.result, self.error
        
        if password not in passwords:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        user_to_change = user_service.get_user_object(user_to_change_public_id)

        if not user_to_change:
            self.error = service_response_builder.not_found_error("User not found")
            return self.result, self.error

        if user_to_change == self.current_user:
            self.error = service_response_builder.validation_error("You cannot change your status only admin can, you are a moderator")
            return self.result, self.error
        
        if user_to_change.role in {"admin", "moderator"}:
            self.error = service_response_builder.forbidden_error("Cannot change the status of admin or moderator only user")
            return self.result, self.error

        if user_to_change.status == status:
            self.error = service_response_builder.conflict_error(message="User already has this status")
            return self.result, self.error

        r  = user_service.update_user_status(user_to_change, status)

        if not r:
            logger.error("An error at moderator_service. Could not change user status")
            self.error = service_response_builder.internal_server_error(message="Could not change user status")
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    user_to_change,
                    content=f"Your status has changed to {status}"
                )
        
        self.result = service_response_builder.result(message="User status has been changed")
        return self.result, self.error