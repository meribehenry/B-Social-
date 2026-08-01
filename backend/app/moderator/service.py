from app.post.service import PostService
from app.comment.service import CommentService
from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from app.notification.service import NotificationService
import os


service_response_builder = ServiceResponseBuilder()
user_service = UserService()

passwords = {os.environ.get("MODERATOR_PASSWORD"), os.environ.get("ADMIN_PASSWORD")}


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

        post = PostService(post_public_id).get_post_object(post_public_id)
        
        _, e = PostService(post_public_id).delete_post(post_public_id)

        if e:
            print(f"An error at moderator_service take_down_post")
            self.error = e
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    post.author.public_id,
                    content=f"You post was taken down for violating community rule",
                )

        self.result = service_response_builder.result(message="Post removed and user has been notified")
        return self.result, self.error
    

    def take_down_comment(self, comment_public_id, data:dict):
        password = data.get("password")
        
        if password not in passwords:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        comment = CommentService(self.current_user.public_id).get_comment_object(comment_public_id)

        _, e = CommentService(self.current_user.public_id).delete_comment(comment_public_id)

        if e:
            print(f"An error at moderator_service take_down_comment")
            self.error = e
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    comment.author.public_id,
                    content=f"You comment was taken down for violating community rule",
                )
        
        self.result = service_response_builder.result(message="Comment removed and user has been notified")
        return self.result, self.error
    

    def change_user_status(self, user_to_change_public_id, data:dict):
        password = data.get("password")
        status = data.get("status")

        if status not in {"suspend", "active"}:
            self.error = service_response_builder.validation_error(message="Invalid status type")
            return self.result, self.error
        
        if password not in passwords:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        user_to_change = user_service.get_user_object(user_to_change_public_id)

        if not user_to_change:
            self.error = service_response_builder.not_found_error("Post not found")
            return self.result, self.error
        
        if user_to_change.role in {"admin", "moderator"}:
            self.error = service_response_builder.forbidden_error("Cannot suspend admin or moderator only user")
            return self.result, self.error

        r  = user_service.update_user_status(user_to_change, status)

        if not r:
            self.error = service_response_builder.internal_server_error(message="Could not change user status")
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    user_to_change.public_id,
                    content=f"You status has changed to {status}"
                )
        
        self.result = service_response_builder.result(message="User status has been changed")
        return self.result, self.error