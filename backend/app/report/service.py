from app.shared.pagination import create_pagination_dict
from app.report.schema import ReportResponseSchema
from app.shared.response import ServiceResponseBuilder
from app.user.service import UserService
from app.report.model import Report
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db, logger


service_response_builder = ServiceResponseBuilder()
user_service = UserService()
report_response_schema = ReportResponseSchema()
reports_response_schema = ReportResponseSchema(many=True)

class ReportService():

    def __init__(self, user_public_id):
        self.current_user = user_service.get_user_object(user_public_id)
        self.error = {}
        self.result = {}
    
    def create_report(self, data:dict,):
        reported_case_id, case_type, reported_case = data.get("reported_case_id"), data.get("case_type"), data.get("reported_case")

        if case_type not in {"post", "comment", "user"}:
            self.error = service_response_builder.validation_error("The report case type must be either ['post', 'comment', 'user']")
            return self.result, self.error

        if case_type == "post":
            from app.post.service import PostService
            post_service = PostService(self.current_user.public_id)
            post_exist = post_service.get_post_object(reported_case_id)
            if not post_exist:
                self.error = service_response_builder.not_found_error(message="The reported post does not exist")
                return self.result, self.error
            if post_exist.user_id == self.current_user.id:
                self.error = service_response_builder.validation_error("You cannot report your own post")
                return self.result, self.error
            
        elif case_type == "comment":
            from app.comment.service import CommentService
            comment_service = CommentService(self.current_user.public_id)
            comment_exist = comment_service.get_comment_object(reported_case_id)
            if not comment_exist:
                self.error = service_response_builder.not_found_error(message="The reported comment does not exist")
                return self.result, self.error
            if comment_exist.user_id == self.current_user.id:
                self.error = service_response_builder.validation_error("You cannot report your own comment")
                return self.result, self.error
        elif case_type == "user":
            user_exist = user_service.get_user_object(reported_case_id)
            if not user_exist:
                self.error = service_response_builder.not_found_error(message="The reported user does not exist")
                return self.result, self.error
            if user_exist.id == self.current_user.id:
                self.error = service_response_builder.validation_error("You cannot report yourself")
                return self.result, self.error
        

        report = Report(case_id=reported_case_id, type=case_type, case=reported_case)

        try:
            db.session.add(report)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to report {case_type} of public_id {reported_case_id}")
            self.error = service_response_builder.internal_server_error(message="Could not create a report")
            return self.result, self.error
        
        except Exception:
            db.session.rollback()
            logger.error(f"Failed to report {case_type} of public_id {reported_case_id}")
            self.error = service_response_builder.internal_server_error(message="Could not create a report")
            return self.result, self.error

        self.result = service_response_builder.result(message="Report sent successfully", status_code=201)
        return self.result, self.error
    

    def view_reports(self, per_page=20, page=1):
        report_pagination = Report.query.order_by(Report.date.desc()).paginate(per_page=per_page, page=page)

        data = {
            "reports": reports_response_schema.dump(report_pagination.items),
            "pagination": create_pagination_dict(report_pagination)
        }

        self.result = service_response_builder.result(data=data)
        return self.result, self.error
    

    def delete_report(self, report_public_id):
        report = Report.query.filter_by(public_id=report_public_id).first()

        if not report:
            self.error = service_response_builder.not_found_error(message="Report not found")
            return self.result, self.error
        
        try:
            db.session.delete(report)
            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            logger.error(f"Failed to delete report")
            self.error = service_response_builder.internal_server_error(message="Could not delete report")
            return self.result, self.error
        
        except Exception:
            db.session.rollback()
            logger.error(f"Failed to delete report")
            self.error = service_response_builder.internal_server_error(message="Could not delete report")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Report deleted successfully")
        return self.result, self.error
        
    
    def view_report(self, report_public_id):
        report = Report.query.filter_by(public_id=report_public_id).first()

        if not report:
            self.error = service_response_builder.not_found_error(message="Report not found")
            return self.result, self.error
        
        self.result = service_response_builder.result(data=report_response_schema.dump(report))
        return self.result, self.error