from app.models import Follower

def get_follower_dict(current_user):
    follower_dict = {}
    follower_dict = {follower.followed_user_id: follower for follower in Follower.query.filter_by(follower_id=current_user.id).all()}
    return follower_dict