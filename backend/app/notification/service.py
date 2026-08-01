from datetime import datetime, timezone
import time
from app.notification.model import Notification
from app.shared.pagination import create_pagination_dict
from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.notification.schema import NotificationResponseSchema, NotificationStreamResponseSchema


service_response_builder = ServiceResponseBuilder()
notification_response_schema = NotificationResponseSchema(many=True)
notification_stream_response_schema = NotificationStreamResponseSchema()

user_service = UserService()


class NotificationService():
    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def create_notification(self, recipient,  content, notification_type="info"):
        notification = Notification(type=notification_type, actor=self.current_user, recipient=recipient, content=content)
        try:
            db.session.add(notification)
            db.session.commit()
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service create_notification\n{e}")
            return None
        
        except Exception as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service create_notification\n{e}")
            return None
        
        
    def delete_notification(self, notification_public_id):
        notification = Notification.query.filter_by(public_id=notification_public_id).first()
        if not notification:
            self.error = service_response_builder.not_found_error(message="Notification not found")
            return self.result, self.error
        
        try:
            db.session.delete(notification)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service delete_notification\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete notification")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service delete_notification\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete notification")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Notification deleted successfully")
        return self.result, self.error
    
    
    def delete_all_notifications(self):
        notifications_count = Notification.query.filter_by(recipient_id=self.current_user.id).delete()

        if not notifications_count:
            self.error = service_response_builder.not_found_error(message="No notification found")
            return self.result, self.error
        
        try:
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service delete_all_notification\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete notifications")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"Sqlalchemy error at notification_service delete_all_notification\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete notifications")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Notifications deleted successfully")
        return self.result, self.error
    
    def _mark_notifications_has_read(self):
        unread_notifications = Notification.query.filter(Notification.is_read==False).all()

        if unread_notifications:
            for notification in unread_notifications:
                notification.is_read = True
            
            try:
                db.session.commit()
            except SQLAlchemyError as e:
                db.session.rollback()
                print(f"Sqlalchemy error at notification_service _mark_notifications_has_read\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could mark notifications has read")
                return self.result, self.error
            
            except Exception as e:
                db.session.rollback()
                print(f"Sqlalchemy error at notification_service _mark_notifications_has_read\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could mark notifications has read")
                return self.result, self.error

        return True, True
        
    def get_notifications(self, per_page=20, page=1):
        notification_pagination = self.current_user.notifications.order_by(Notification.date_created.desc()).paginate(per_page=per_page, page=page)
        data = {
            "notications": notification_response_schema.dump(notification_pagination.items),
            "pagination": create_pagination_dict(notification_pagination)
        }
        self._mark_notifications_has_read()

        self.result = service_response_builder.result(data=data)
        return self.result, self.error
    
    
    def get_notification_count(self):
        notification_count = self.current_user.notifications.filter(Notification.is_read==False).count()
        data = {"notication_count": notification_count}

        self.result = service_response_builder.result(data=data)
        return self.result, self.error

    def notification_event_stream(self):
        last_check = datetime.now(timezone.utc)
        while True:
            new_notifications = Notification.query.filter(
                Notification.recipient_id==self.current_user.id,
                Notification.date_created > last_check
            ).all()

            for notification in new_notifications:
                yield f"data: {notification_stream_response_schema.dump(notification)}\n\n"

            last_check = datetime.now(timezone.utc)
            time.sleep(3)  # Sleep for a short duration to avoid busy waiting