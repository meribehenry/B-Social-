from sqlalchemy.exc import SQLAlchemyError
from app.models.post import Post
from app.models.reaction import PostReaction
from app.models.user import User
from app.extensions import db
from app.utils.response import ServiceResponseBuilder


service_response_builder = ServiceResponseBuilder()

class PostReactionService():
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
        

    def like_post(self, post_public_id):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error 
        
        post_reaction = PostReaction.query.filter_by(post_id=post.id, user_id=self.current_user.id).first()

        if post_reaction and post_reaction.disliked:
            post_reaction.liked = True
            post_reaction.disliked = False
            post.num_of_likes = post.num_of_likes + 1
            post.num_of_dislikes = post.num_of_dislikes - 1

            try:
                db.session.commit()
                self.result = service_response_builder.result()
                return self.result, self.error
            
            except SQLAlchemyError as e:
                post.num_of_likes = post.num_of_likes - 1
                post.num_of_dislikes = post.num_of_dislikes + 1
                db.session.rollback()
                print(f"SQLAlchemy error at post_reaction_service, like_post\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not like post")
                return self.result, self.error
            
            except Exception as e:
                post.num_of_likes = post.num_of_likes - 1
                post.num_of_dislikes = post.num_of_dislikes + 1
                db.session.rollback()
                print(f"An error at post_reaction_service, like_post\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not like post")
                return self.result, self.error
        
        elif not post_reaction:
            post_reaction = PostReaction(liked=True,  disliked=False, post=post, user_id=self.current_user.id)
            post.num_of_likes = post.num_of_likes + 1
            
            try:
                db.session.add(post_reaction)
                db.session.commit()
                self.result = service_response_builder.result(status_code=201)
                return self.result, self.error

            except SQLAlchemyError as e:
                post.num_of_likes = post.num_of_likes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at post_reaction_service, like_post\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not like post")
                return self.result, self.error
            
            except Exception as e:
                post.num_of_likes = post.num_of_likes - 1
                db.session.rollback()
                print(f"An error at post_reaction_service, like_post\n{e}")
                self.error = service_response_builder.internal_server_error(message="Could not like post")
                return self.result, self.error     
        
        else:
            delete_result = self.delete_reaction(post_reaction)
            if delete_result:
                post.num_of_likes = post.num_of_likes - 1
                try:
                    db.session.commit()
                    self.result = service_response_builder.result()
                    return self.result, self.error

                except SQLAlchemyError as e:
                    post.num_of_likes = post.num_of_likes + 1
                    db.session.rollback()
                    print(f"SQLAlchemy error at post_reaction_service, like_post\n{e}")
                    self.error = service_response_builder.internal_server_error(message="Could not unlike post")
                    return self.result, self.error
                
                except Exception as e:
                    post.num_of_likes = post.num_of_likes + 1
                    db.session.rollback()
                    print(f"An error at post_reaction_service, like_post\n{e}")

            self.error = service_response_builder.internal_server_error(message="Could not unlike post")
            return self.result, self.error


    def dislike_post(self, post_public_id):
        post = Post.query.filter_by(public_id=post_public_id).first()

        if not post:
            self.error = service_response_builder.not_found_error(message="Post not found")
            return self.result, self.error
        
        post_reaction = PostReaction.query.filter_by(post_id=post.id, user_id=self.current_user.id).first()

        if post_reaction and post_reaction.liked:
            post_reaction.liked = False
            post_reaction.disliked = True
            post.num_of_likes = post.num_of_likes - 1     
            post.num_of_dislikes = post.num_of_dislikes + 1

            try:
                db.session.commit()
                self.result = service_response_builder.result()
                return self.result, self.error

            except SQLAlchemyError as e:
                post.num_of_likes = post.num_of_likes + 1
                post.num_of_dislikes = post.num_of_dislikes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at post_reaction_service, dislike_post\n{e}")
                self.error = service_response_builder.result(message="Could not dislike post")
                return self.result, self.error
            
            except Exception as e:
                post.num_of_likes = post.num_of_likes + 1
                post.num_of_dislikes = post.num_of_dislikes - 1
                db.session.rollback()
                print(f"An error at post_reaction_service, dislike_post\n{e}")
                self.error = service_response_builder.result(message="Could not dislike post")
                return self.result, self.error

        elif not post_reaction:
            post_reaction = PostReaction(liked=False, disliked=True, post=post, user_id=self.current_user.id)
            post.num_of_dislikes = post.num_of_dislikes + 1
            
            try:
                db.session.add(post_reaction)
                db.session.commit()
                self.result = service_response_builder.result(status_code=201)
                return self.result, self.error

            except SQLAlchemyError as e:
                post.num_of_likes = post.num_of_dislikes - 1
                db.session.rollback()
                print(f"SQLAlchemy error at post_reaction_service, dislike_post\n{e}")
                self.error = service_response_builder.result(message="Could not dislike post")
                return self.result, self.error
            
            except Exception as e:
                post.num_of_likes = post.num_of_dislikes - 1
                db.session.rollback()
                print(f"An error at post_reaction_service, dislike_post\n{e}")
                self.error = service_response_builder.result(message="Could not dislike post")
                return self.result, self.error
        
        else:
            delete_result = self.delete_reaction(post_reaction)
            if delete_result:
                post.num_of_dislikes = post.num_of_dislikes - 1
                try:
                    db.session.commit()
                    self.result = service_response_builder.result()
                    return self.result, self.error
                
                except SQLAlchemyError as e:
                    post.num_of_dislikes = post.num_of_dislikes + 1
                    db.session.rollback()
                    print(f"SQLAlchemy error at post_reaction_service, dislike_post\n{e}")
                    self.error = service_response_builder.result(message="Could not undislike post")
                    return self.result, self.error
                
                except Exception as e:
                    post.num_of_dislikes = post.num_of_dislikes + 1
                    db.session.rollback()
                    print(f"An error at post_reaction_service, dislike_post\n{e}")
                    self.error = service_response_builder.result(message="Could not undislike post")
                    return self.result, self.error