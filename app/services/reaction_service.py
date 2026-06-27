from sqlalchemy.exc import SQLAlchemyError
from app.models import PostReaction, CommentReaction
from app.extensions import db

class ReactionService():

    def delete_reaction(self, reaction):
        try:
            db.session.delete(reaction)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return None

        return True

    def like_post(self, post, current_user):
        post_reaction = PostReaction.query.filter_by(post_id=post.id, user_id=current_user.id).first()

        if post_reaction and post_reaction.disliked:
            post_reaction.liked = True
            post_reaction.disliked = False
            post.num_of_likes = post.num_of_likes + 1
            post.num_of_dislikes = post.num_of_dislikes - 1

            try:
                db.session.commit()
            except SQLAlchemyError:
                post.num_of_likes = post.num_of_likes - 1
                post.num_of_dislikes = post.num_of_dislikes + 1
                db.session.rollback()
                return None
            
            return post_reaction
        
        elif not post_reaction:
            post_reaction = PostReaction(liked=True,  disliked=False, post=post, user_id=current_user.id, username=current_user.username)
            post.num_of_likes = post.num_of_likes + 1
            
            try:
                db.session.add(post_reaction)
                db.session.commit()
            except SQLAlchemyError:
                post.num_of_likes = post.num_of_likes - 1
                db.session.rollback()
                return None
            
            return post_reaction
        
        else:
            result = self.delete_reaction(post_reaction)
            if result:
                post.num_of_likes = post.num_of_likes - 1
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    post.num_of_likes = post.num_of_likes + 1
                    db.session.rollback()
                    return None
                return "deleted"



    def dislike_post(self, post, current_user):
        post_reaction = PostReaction.query.filter_by(post_id=post.id, user_id=current_user.id).first()

        if post_reaction and post_reaction.liked:
            post_reaction.liked = False
            post_reaction.disliked = True
            post.num_of_likes = post.num_of_likes - 1
            post.num_of_dislikes = post.num_of_dislikes + 1

            try:
                db.session.commit()
            except SQLAlchemyError:
                post.num_of_likes = post.num_of_likes + 1
                post.num_of_dislikes = post.num_of_dislikes - 1
                db.session.rollback()
                return None
            
            return post_reaction

        elif not post_reaction:
            post_reaction = PostReaction(liked=False, disliked=True, post=post, user_id=current_user.id, username=current_user.username)
            post.num_of_dislikes = post.num_of_dislikes + 1
            
            try:
                db.session.add(post_reaction)
                db.session.commit()
            except SQLAlchemyError:
                post.num_of_likes = post.num_of_dislikes - 1
                db.session.rollback()
                return None
            
            return post_reaction
        
        else:
            result = self.delete_reaction(post_reaction)
            if result:
                post.num_of_dislikes = post.num_of_dislikes - 1
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    post.num_of_dislikes = post.num_of_dislikes + 1
                    db.session.rollback()
                    return None
                return "deleted"


    def like_comment(self, comment, current_user):
        comment_reaction =  CommentReaction.query.filter_by(comment_id=comment.id, user_id=current_user.id).first()

        if comment_reaction and comment_reaction.disliked:
            comment_reaction.liked = True
            comment_reaction.disliked = False
            comment.num_of_likes = comment.num_of_likes + 1
            comment.num_of_dislikes = comment.num_of_dislikes - 1

            try:
                db.session.commit()
            except SQLAlchemyError:
                comment.num_of_likes = comment.num_of_likes - 1
                comment.num_of_dislikes = comment.num_of_dislikes + 1
                db.session.rollback()
                return None
            
            return comment_reaction

        elif not comment_reaction:
            comment_reaction = CommentReaction(liked=True,  disliked=False, comment=comment, post_id=comment.post_id, user_id=current_user.id, username=current_user.username)
            comment.num_of_likes = comment.num_of_likes + 1

            try:
                db.session.add(comment_reaction)
                db.session.commit()
            except SQLAlchemyError:
                comment.num_of_likes = comment.num_of_likes - 1
                db.session.rollback()
                return None
            
            return comment_reaction
        
        else:
            result = self.delete_reaction(comment_reaction)
            if result:
                comment.num_of_likes = comment.num_of_likes - 1
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    comment.num_of_likes = comment.num_of_likes + 1
                    db.session.rollback()
                    return None
                return "deleted"
            

    def dislike_comment(self, comment, current_user):
        comment_reaction =  CommentReaction.query.filter_by(comment_id=comment.id, user_id=current_user.id).first()

        if comment_reaction and comment_reaction.liked:
            comment_reaction.liked = False
            comment_reaction.disliked = True
            comment.num_of_likes = comment.num_of_likes - 1
            comment.num_of_dislikes = comment.num_of_dislikes + 1

            try:
                db.session.commit()
            except SQLAlchemyError:
                comment.num_of_likes = comment.num_of_likes + 1
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                return None
            
            return comment_reaction
        
        elif not comment_reaction:
            comment_reaction = CommentReaction(liked=False,  disliked=True, comment=comment, post_id=comment.post_id, user_id=current_user.id, username=current_user.username)
            comment.num_of_dislikes = comment.num_of_dislikes + 1

            try:
                db.session.add(comment_reaction)
                db.session.commit()
            except SQLAlchemyError:
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                db.session.rollback()
                return None
            
            return comment_reaction
        
        else:
            result = self.delete_reaction(comment_reaction)
            if result:
                comment.num_of_dislikes = comment.num_of_dislikes - 1
                try:
                    db.session.commit()
                except SQLAlchemyError:
                    comment.num_of_dislikes = comment.num_of_dislikes + 1
                    db.session.rollback()
                    return None
                return "deleted"