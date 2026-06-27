def get_user_post_reactions_dict(current_user):
    reacted_post = {}
    reacted_post = {reaction.post_id: reaction for reaction in current_user.post_reaction.all()}
    return reacted_post

def get_user_comment_reactions_dict(current_user):
    reacted_comment = {}
    reacted_comment = {reaction.comment_id: reaction for reaction in current_user.comment_reaction.all()}
    return reacted_comment