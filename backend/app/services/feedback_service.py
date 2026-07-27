from app.extensions import db
from app.models.feedback import Feedback
from app.models.user import User
from sqlalchemy.exc import SQLAlchemyError
from app.utils.sanitise import sanitise
from app.utils.pagination import create_pagination_dict
from app.utils.response import ServiceResponseBuilder
from app.schemas.feedback import FeedbackResponseSchema


feedbacks_response_schema = FeedbackResponseSchema(many=True)
service_response_builder = ServiceResponseBuilder()


class FeedbackService:
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first_or_404()
        self.error = {}
        self.result = {}

    def submit_feedback(self, data:dict):
        content = sanitise(data.get("content"))

        if not content:
            self.error = service_response_builder.bad_request_error(message="Invaild request. Please fill in the field")
            return self.result, self.error

        feedback = Feedback(writer_id=self.current_user.id, content=content) 
                        
        try:
            db.session.add(feedback)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at feedback_service, submit_feedback\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not submit feedback")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at feedback_service, submit_feedback\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not submit feedback")
            return self.result, self.error

        self.result = service_response_builder.result(message="Successfully submitted feedback", status_code=201)
        return self.result, self.error
    
    
    def delete_feedback(self, feedback_public_id):
        feedback = Feedback.query.filter_by(public_id=feedback_public_id).first()

        if not feedback:
            self.error = service_response_builder.not_found_error(message="Feedback not found")
            return self.result, self.error
        
        try:
            db.session.delete(feedback)
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at feedback_service, delete_feedback\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete feedback")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at feedback_service, delete_feedback\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete feedback")
            return self.result, self.error

        self.result = service_response_builder.result(message="Successfully deleted feedback")
        return self.result, self.error
    

    def view_feedbacks(self, per_page=20, page=1):
        feedback_pagination = Feedback.query.order_by(Feedback.date_created.desc()).paginate(per_page=per_page, page=page)

        data = {
            "feedbacks": feedbacks_response_schema.dump(feedback_pagination.items),
            "pagination": create_pagination_dict(feedback_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error