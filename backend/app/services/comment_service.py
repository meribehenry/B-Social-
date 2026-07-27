from app.models.comment import Comment
from app.models.user import User
from app.models.post import Post
from app.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from app.utils.sanitise import sanitise
from app.utils.response import  ServiceResponseBuilder
from app.schemas.comment import CommentResponseSchema

comment_response_schema = CommentResponseSchema()
service_response_builder = ServiceResponseBuilder()


class CommentService():
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first()
        self.error = {}
        self.result = {}
    
    def create_comment(self, post_public_id, data:dict):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 
        
        content = sanitise(data.get("content"))

        if not content:
            self.error = service_response_builder.bad_request_error(message="Comment field cannot be empty")
            return self.result, self.error 
            
        comment = Comment(content=content, user_id=self.current_user.id, post=post)
        post.num_of_comments = post.num_of_comments + 1

        try:
            db.session.add(comment)
            db.session.commit()

        except SQLAlchemyError as e:
            post.num_of_comments = post.num_of_comments - 1
            db.session.rollback()
            print(f"Sqlalchemy error at comment_service, create_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create comment")
            return self.result, self.error
        
        except Exception as e:
            post.num_of_comments = post.num_of_comments - 1
            db.session.rollback()
            print(f"An error at comment_service, create_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not create comment")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Comment created successfully", 
                                                      data= comment_response_schema.dump(comment),
                                                      status_code=201)

        return self.result, self.error
    
    def edit_comment(self, comment_public_id, data:dict):
        comment = Comment.query.filter_by(public_id=comment_public_id).first_or_404()
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 
        
        new_content = sanitise(data.get("content"))

        if not new_content or new_content == comment.content:
            self.error = service_response_builder.bad_request_error(message="Comment field cannot be empty or left the same")
            return self.result, self.error 
        
        comment.content = new_content

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, edit_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update comment")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"An error at comment_service, edit_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not update comment")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Comment successfully updated", 
                                                      data= comment_response_schema.dump(comment))
        
        return self.result, self.error
        
    
    def delete_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id)
        
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        comment.post.num_of_comments = comment.post.num_of_comments - 1
        
        try:
            db.session.delete(comment)
            db.session.commit()

        except SQLAlchemyError as e:
            comment.post.num_of_comments = comment.post.num_of_comments + 1
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, delete_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete comment")
            return self.result, self.error
        
        except Exception as e:
            db.session.rollback()
            print(f"SQLAlchemy error at comment_service, delete_comment\n{e}")
            self.error = service_response_builder.internal_server_error(message="Could not delete comment")
            return self.result, self.error
        
        self.result = service_response_builder.result(message="Comment successfully deleted")
        return self.result, self.error
    

    def view_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()

        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        self.result = service_response_builder.result(data= comment_response_schema.dump(comment))
        return self.result, self.error