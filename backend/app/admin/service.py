from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from app.notification.service import NotificationService
import os


service_response_builder = ServiceResponseBuilder()
user_service = UserService()

admin_password = os.environ.get("ADMIN_PASSWORD")
creator_password = os.environ.get("CREATOR_PASSWORD")


class AdminService():

    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def change_user_role(self, username, data:dict):
        password = data.get("password")
        role = data.get("role")
        
        user = user_service.get_user_object(username, retrival_method="username")

        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        if password == admin_password and user.role != "admin":
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        r = user_service.update_user_role(user, role)
        if not r:
            print(f"An error at admin_service change_user_role")
            self.error = service_response_builder.internal_server_error(message="Could not change user role")
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    post.author.public_id,
                    content=f"You role has been changed to {role}",
                )
        self.result = service_response_builder.result(message="User role has been changed")
        return self.result, self.error


    def change_user_status(self, username, data:dict):
        password = data.get("password")
        status = data.get("status")

        if status not in {"suspend", "active"}:
            self.error = service_response_builder.validation_error(message="Invalid status type")
            return self.result, self.error

        user_to_change = user_service.get_user_object(username, retrival_method="username")

        if not user_to_change:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error
        
        if password != creator_password or password != admin_password:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        if user_to_change.role == "admin" and password != creator_password:
            self.error = service_response_builder.forbidden_error("Cannot suspend admin only the creator can")
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