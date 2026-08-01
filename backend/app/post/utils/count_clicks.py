from app.post.models.click import Click


def count_clicks(post, current_user):
    click = Click.query.filter_by(post_id=post.id, user_id=current_user.id).first()

    if not click:
        if post.author != current_user:
            click = Click(post_id=post.id, viewed=True, user_id=current_user.id)
            click.viewed = True
            from app.post.service import PostService
            PostService(post.author.public_id).update_count(current_user, type_of_count="clicks")
            return True