from sqlalchemy.exc import SQLAlchemyError
from app.models.comment import Comment
from app.models.reaction import  CommentReaction
from app.models.user import User
from app.extensions import db
from app.utils.response import ServiceResponseBuilder


service_response_builder = ServiceResponseBuilder()

class CommentReactionService():
    def __init__(self, user_public_id):
        self.current_user = User.query.filter_by(public_id=user_public_id).first_or_404()
        self.error = {}
        self.result = {}
    
    def delete_reaction(self, reaction):
        try:
            db.session.delete(reaction)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            return None
        

    def like_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()
        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 

        comment_reaction =  CommentReaction.query.filter_by(comment_id=comment.id, user_id=self.current_user.id).first()

        if comment_reaction and comment_reaction.disliked:
            comment_reaction.liked = True
            comment_reaction.disliked = False
            comment.num_of_likes = comment.num_of_likes + 1
            comment.num_of_dislikes = comment.num_of_dislikes - 1

            try:
                db.session.commit()
                self.result = service_response_builder.result()
                return self.result, self.error

            except SQLAlchemyError as e:
                comment.num_of_likes = comment.num_of_likes - 1
                comment.num_of_dislikes = comment.num_of_dislikes + 1
                db.session.rollback()
                print(f"SQLAlchemy error at comment_reaction_service, like_comment\n{e}")
                self.error = service_response_builder.internal_server_error("Could not like comment")
                return self.result, self.error
            
            except Exception as e:
                comment.num_of_likes = comment.num_of_likes - 1
                comment.num_of_dislikes = comment.num_of_dislikes + 1
                db.session.rollback()
                print(f"An error at comment_reaction_service, like_comment\n{e}")
                self.error = service_response_builder.internal_server_error("Could not like comment")
                return self.result, self.error

        elif not comment_reaction:
            comment_reaction = CommentReaction(liked=True,  disliked=False, comment=comment, post_id=comment.post_id, user_id=self.current_user.id)
            comment.num_of_likes = comment.num_of_likes + 1

            try:
                db.session.add(comment_reaction)
                db.session.commit()
                self.result = service_response_builder.result(status_code=201)
                return self.result, self.error

            except SQLAlchemyError as e:
                comment.num_of_likes = comment.num_of_likes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at comment_reaction_service, like_comment\n{e}")
                self.error = service_response_builder.internal_server_error("Could not like comment")
                return self.result, self.error
            
            except Exception as e:
                comment.num_of_likes = comment.num_of_likes - 1
                db.session.rollback()
                print(f"An error at comment_reaction_service, like_comment\n{e}")
                self.error = service_response_builder.internal_server_error("Could not like comment")
                return self.result, self.error
        
        else:
            delete_result = self.delete_reaction(comment_reaction)
            if delete_result:
                comment.num_of_likes = comment.num_of_likes - 1
                try:
                    db.session.commit()
                    self.result = service_response_builder.result()
                    return self.result, self.error

                except SQLAlchemyError as e:
                    comment.num_of_likes = comment.num_of_likes + 1
                    db.session.rollback()
                    print(f"SQLAlchemy error at comment_reaction_service, like_comment\n{e}")
                    self.error = service_response_builder.internal_server_error("Could not unlike comment")
                    return self.result, self.error
                
                except Exception as e:
                    comment.num_of_likes = comment.num_of_likes + 1
                    db.session.rollback()
                    print(f"An error at comment_reaction_service, like_comment\n{e}")

            self.error = service_response_builder.internal_server_error("Could not unlike comment")
            return self.result, self.error
            

    def dislike_comment(self, comment_public_id):
        comment = Comment.query.filter_by(public_id=comment_public_id).first()

        if not comment:
            self.error = service_response_builder.not_found_error(message="Comment not found")
            return self.result, self.error 
        
        comment_reaction =  CommentReaction.query.filter_by(comment_id=comment.id, user_id=self.current_user.id).first()

        if comment_reaction and comment_reaction.liked:
            comment_reaction.liked = False
            comment_reaction.disliked = True
            comment.num_of_likes = comment.num_of_likes - 1
            comment.num_of_dislikes = comment.num_of_dislikes + 1

            try:
                db.session.commit()
                self.result = service_response_builder.result()
                return self.result, self.error

            except SQLAlchemyError as e:
                comment.num_of_likes = comment.num_of_likes + 1
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at comment_reaction_service, dislike_comment\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not dislike comment")
            
            except Exception as e:
                comment.num_of_likes = comment.num_of_likes + 1
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                print(f"An error at comment_reaction_service, dislike_comment\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not dislike comment")
                return self.result, self.error
        
        elif not comment_reaction:
            comment_reaction = CommentReaction(liked=False,  disliked=True, comment=comment, post_id=comment.post_id, user_id=self.current_user.id)
            comment.num_of_dislikes = comment.num_of_dislikes + 1

            try:
                db.session.add(comment_reaction)
                db.session.commit()
                self.result = service_response_builder.result(status_code=201)
                return self.result, self.error

            except SQLAlchemyError as e:
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at comment_reaction_service, dislike_comment\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not dislike comment")
                return self.result, self.error
            
            except Exception as e:
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                print(f"An error at comment_reaction_service, dislike_comment\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not dislike comment")
                return self.result, self.error
        
        else:
            delete_result = self.delete_reaction(comment_reaction)
            if delete_result:
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                try:
                    db.session.commit()
                    self.result = service_response_builder.result()
                    return self.result, self.error

                except SQLAlchemyError as e:
                    comment.num_of_dislikes = comment.num_of_dislikes + 1
                    db.session.rollback()
                    print(f"SQLAlchemy error at comment_reaction_service, dislike_comment\n{e}")
                    self.error = service_response_builder.internal_server_error(message="Could not undislike comment")
                    return self.result, self.error
                
                except Exception as e:
                    comment.num_of_dislikes = comment.num_of_dislikes + 1
                    db.session.rollback()
                    print(f"An error at comment_reaction_service, dislike_comment\n{e}")

            self.error = service_response_builder.internal_server_error(message="Could not undislike comment")
            return self.result, self.error