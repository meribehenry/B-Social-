from flask import Blueprint, abort, redirect, render_template, request, url_for, flash
from app.models import User, Post
from app.extensions import db
from flask_login import current_user, login_required
from .utils import save_profile_pic, delete_profile_pic

from app.profile.forms import EditProfileForm


profile = Blueprint("profile", __name__)


@profile.route("/view/<int:user_id>")
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    page = request.args.get("page", 1, type=int)
    posts = user.posts.order_by(Post.date_created.desc()).paginate(page=page, per_page=20)
    return render_template("profile/view_profile.html", posts=posts, user=user, title="Profile")


@profile.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)

    if current_user != user:
        abort(403, "You are not authorized to do this")
    
    form = EditProfileForm()

    if form.validate_on_submit():

        if form.profile_pic.data:

            if user.profile_pic_id:
                delete_profile_pic(user.profile_pic_id)
                user.profile_pic_url, user.profile_pic_id = save_profile_pic(form.profile_pic.data)

        current_user.bio = form.bio.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.username.data

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "error")
            return redirect(url_for("profile.edit_profile", user_id=current_user.id))
        
        flash("Profile successfully updated", "success")
        return redirect(url_for("profile.view_profile", user_id=current_user.id ))
    
    elif request.method == "GET":
        form.bio.data =  current_user.bio 
        form.firstname.data = current_user.firstname 
        form.lastname.data = current_user.lastname
        form.username.data = current_user.username 
    
    return render_template("profile/edit_profile.html", form=form, title="Edit Profile")
