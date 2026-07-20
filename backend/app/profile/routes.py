from flask import Blueprint, abort, redirect, render_template, request, url_for
from app.models import Follower, User, Post
from flask_login import current_user, login_required
from app.services.follower_service import FollowerService
from app.services.profile_service import ProfileService
from app.profile.forms import EditProfileForm
from app.utils.reaction_dict import get_user_post_reactions_dict
from app.utils.decorators import verification_required
from app.utils.follower_dict import get_follower_dict


profile = Blueprint("profile", __name__)


@profile.route("/view/<user_public_id>")
@login_required
@verification_required
def view_profile(user_public_id):
    user = User.query.filter_by(public_id=user_public_id).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.date_created.desc()).paginate(page=page, per_page=20)

    if request.args.get("follower", type=str):
        follower_service = FollowerService(current_user)
        follower  =  request.args.get("follower", type=str)

        if follower == "follow":
            follower_service.follow_user(user)
        else:
            follower_service.unfollow_user(user)

        return redirect(url_for("profile.view_profile", user_public_id=user.public_id))
    
    follower_object = None
    if current_user != user:
        follower_object = Follower.query.filter_by(follower_id=current_user.id, followed_user_id=user.id).first()
    post_reactions_dict = get_user_post_reactions_dict(current_user)
    follower_dict = get_follower_dict(current_user)
    return render_template("profile/view_profile.html", posts=posts, user=user, title="Profile", follower=follower_object, post_reactions_dict=post_reactions_dict, follower_dict=follower_dict)


@profile.route("/edit/<user_public_id>", methods=["GET", "POST"])
@login_required
@verification_required
def edit_profile(user_public_id):
    user = User.query.filter_by(public_id=user_public_id).first_or_404()

    if current_user != user:
        abort(403, "You are not authorized to do this")
    
    form = EditProfileForm()
    profile_service = ProfileService(current_user)

    if form.validate_on_submit():
        result = profile_service.edit_profile(form, current_user)

        if not result:
            return redirect(url_for("profile.edit_profile", user_public_id=current_user.public_id))
        
        return redirect(url_for("profile.view_profile", user_public_id=current_user.public_id))
    
    elif request.method == "GET":
        profile_service = ProfileService(current_user)
        form = profile_service.populate_form(form)
    
    return render_template("profile/edit_profile.html", form=form, title="Edit Profile")