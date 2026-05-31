from app.models import LikePost, LikeComment
from app.extensions import db


def delete_post_reaction(post_reaction):
    db.session.delete(post_reaction)
    db.session.commit()

def delete_comment_reaction(comment_reaction):
    db.session.delete(comment_reaction)
    db.session.commit()

def like_post(post, current_user):
    post_reaction = LikePost.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if post_reaction and post_reaction.disliked:
        post_reaction.liked = True
        post_reaction.disliked = False

        try:
            post.num_of_likes = post.num_of_likes + 1
            post.num_of_dislikes = post.num_of_dislikes - 1
            db.session.commit()
        except Exception:
            return None
        
        return post_reaction
    
    elif not post_reaction:
        post_reaction = LikePost(liked=True,  disliked=False, post=post, user_id=current_user.id, username=current_user.username)

        try:
            db.session.add(post_reaction)
            post.num_of_likes = post.num_of_likes + 1
            db.session.commit()
        except Exception:
            return None
        
        return post_reaction
    
    else:
        post.num_of_likes = post.num_of_likes - 1
        delete_post_reaction(post_reaction)


def dislike_post(post, current_user):
    post_reaction = LikePost.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if post_reaction and post_reaction.liked:
        post_reaction.liked = False
        post_reaction.disliked = True

        try:
            post.num_of_likes = post.num_of_likes - 1
            post.num_of_dislikes = post.num_of_dislikes + 1
            db.session.commit()
        except Exception:
            return None
        
        return post_reaction

    elif not post_reaction:
        post_reaction = LikePost(liked=False, disliked=True, post=post, user_id=current_user.id, username=current_user.username)

        try:
            db.session.add(post_reaction)
            post.num_of_dislikes = post.num_of_dislikes + 1
            db.session.commit()
        except Exception:
            return None
        
        return post_reaction
    
    else:
        post.num_of_dislikes = post.num_of_dislikes - 1
        delete_post_reaction(post_reaction)


def like_comment(comment, current_user):
    comment_reaction =  LikeComment.query.filter_by(comment_id=comment.id, user_id=current_user.id).first()

    if comment_reaction and comment_reaction.disliked:
        comment_reaction.liked = True
        comment_reaction.disliked = False

        try:
            comment.num_of_likes = comment.num_of_likes + 1
            comment.num_of_dislikes = comment.num_of_dislikes - 1
            db.session.commit()
        except Exception:
            return None
        
        return comment_reaction

    elif not comment_reaction:
        comment_reaction = LikeComment(liked=True,  disliked=False, comment=comment, post_id=comment.post_id, user_id=current_user.id, username=current_user.username)

        try:
            db.session.add(comment_reaction)
            comment.num_of_likes = comment.num_of_likes + 1
            db.session.commit()
        except Exception:
            return None
        
        return comment_reaction
    
    else:
        comment.num_of_likes = comment.num_of_likes - 1
        delete_comment_reaction(comment_reaction)


def dislike_comment(comment, current_user):
    comment_reaction =  LikeComment.query.filter_by(comment_id=comment.id, user_id=current_user.id).first()

    if comment_reaction and comment_reaction.liked:
        comment_reaction.liked = False
        comment_reaction.disliked = True

        try:
            comment.num_of_likes = comment.num_of_likes - 1
            comment.num_of_dislikes = comment.num_of_dislikes + 1
            db.session.commit()
        except Exception:
            return None
        
        return comment_reaction
    
    elif not comment_reaction:
        comment_reaction = LikeComment(liked=False,  disliked=True, comment=comment, post_id=comment.post_id, user_id=current_user.id, username=current_user.username)

        try:
            db.session.add(comment_reaction)
            comment.num_of_dislikes = comment.num_of_dislikes + 1
            db.session.commit()
        except Exception:
            return None
        
        return comment_reaction
    
    else:
        comment.num_of_dislikes = comment.num_of_dislikes - 1
        delete_comment_reaction(comment_reaction)