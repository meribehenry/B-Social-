from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from app.notification.service import NotificationService
from app.extensions import logger
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
    
    def change_user_role(self, data:dict):
        password = data.get("password")
        role = data.get("role")
        username = data.get("username")

        if role not in ["user", "admin", "moderator"]:
            self.error = service_response_builder.validation_error(message="Invalid role type")
            return self.result, self.error
        
        user = user_service.get_user_object(username, retrival_method="username")

        if not user:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error

        if user == self.current_user:
            self.error = service_response_builder.validation_error("You cannot change your role you are an admin")
            return self.result, self.error

        if password != admin_password and password != creator_password:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error

        if password != creator_password and (user.role == "admin" or role=="admin") :
            self.error = service_response_builder.forbidden_error("You cannot change role of an admin or make a user an admin, only the creator can")
            return self.result, self.error  

        if role == user.role:
            self.error = service_response_builder.conflict_error(message="User already has this role")
            return self.result, self.error

        r = user_service.update_user_role(user.public_id, role)

        if not r:
            logger.error("An error at admin_service change_user_role")
            self.error = service_response_builder.internal_server_error(message="Could not change user role")
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    user,
                    content=f"You role has been changed to {role}",
                )
        self.result = service_response_builder.result(message="User role has been changed")
        return self.result, self.error


    def change_user_status(self, public_id, data:dict):
        password = data.get("password")
        status = data.get("status")

        if status not in {"suspended", "active"}:
            self.error = service_response_builder.validation_error(message="Invalid status type")
            return self.result, self.error

        user_to_change = user_service.get_user_object(public_id)

        if not user_to_change:
            self.error = service_response_builder.not_found_error(message="User not found")
            return self.result, self.error

        if user_to_change == self.current_user:
            self.error = service_response_builder.validation_error("You cannot change your status you are an admin")
            return self.result, self.error

        if password != creator_password and password != admin_password:
            self.error = service_response_builder.validation_error("Invalid password. Please enter a correct password")
            return self.result, self.error
        
        if password != creator_password and user_to_change.role == "admin":
            self.error = service_response_builder.forbidden_error("You cannot change status of an admin only the creator can")
            return self.result, self.error

        if user_to_change.status == status:
            self.error = service_response_builder.conflict_error(message="User already has this status")
            return self.result, self.error
        
        r  = user_service.update_user_status(user_to_change, status)

        if not r:
            logger.error("An error at admin_service change_user_status")
            self.error = service_response_builder.internal_server_error(message="Could not change user status")
            return self.result, self.error
        
        NotificationService(self.current_user.public_id).create_notification(
                    user_to_change,
                    content=f"You status has changed to {status}"
                )
        
        self.result = service_response_builder.result(message="User status has been changed")
        return self.result, self.error