from flask import Blueprint, render_template, redirect, request, url_for, abort
from app.models import Follower, Post, Comment
from .forms import NewPostForm
from flask_login import login_required, current_user
from app.utils.count_clicks import count_clicks
from app.services.post_service import PostService
from app.services.reaction_service import ReactionService
from app.utils.decorators import verification_required
from app.utils.reaction_dict import get_user_comment_reactions_dict, get_user_post_reactions_dict

posts = Blueprint("posts", __name__)


@posts.route("/new_post", methods=["GET", "POST"])
@login_required
@verification_required
def new_post():
    form = NewPostForm()

    if form.validate_on_submit():
        post_service = PostService(current_user)
        result = post_service.create_post(form)

        if result is None:
            return redirect(url_for("posts.new_post"))
        
        return redirect(url_for("main.home"))

    return render_template("posts/new_post.html", form=form, title="New Post")


@posts.route("/update/<post_public_id>", methods=["GET", "POST"])
@login_required
@verification_required
def update_post(post_public_id):
    post = Post.query.filter_by(public_id=post_public_id).first_or_404()
    if post.author != current_user:
        abort(403)

    form = NewPostForm()

    if form.validate_on_submit():
        post_service = PostService(current_user)
        result = post_service.edit_post(form, post)

        if result is None:
            return redirect(url_for("posts.update_post", post_public_id=post.public_id))  
        else:
            return redirect(url_for("posts.view_post", post_public_id=post.public_id))
    
    elif request.method == "GET":
        form.content.data = post.content
    
    return render_template("posts/new_post.html", form=form, title="Update Post",post=post, photo_url=post.photo_url if post.photo_url else None)
        

@posts.route("/view/<post_public_id>", methods=["GET", "POST"])
@login_required
@verification_required
def view_post(post_public_id):
    post = Post.query.filter_by(public_id=post_public_id).first_or_404()
    count_clicks(post, current_user)
    
    if request.args.get("reaction", type=str):
        reaction = request.args.get("reaction", type=str)
        reaction_service = ReactionService()
      
        if reaction == "like":
            reaction_service.like_post(post, current_user)
        else:
            reaction_service.dislike_post(post, current_user)

        return redirect(url_for("posts.view_post", post_public_id=post.public_id))
    
    page = request.args.get("page", 1, type=int)
    comments = post.comments.order_by(Comment.date_created.desc()).paginate(page=page, per_page=20)
    comment_reactions_dict =  get_user_comment_reactions_dict(current_user)
    post_reactions_dict = get_user_post_reactions_dict(current_user)
    follower_object = None
    
    follower_object = Follower.query.filter_by(follower_id=current_user.id, followed_user_id=post.author.id).first()
    return render_template("posts/view_post.html", 
                            post=post, 
                            title="View Post", 
                            comments=comments, 
                            comment_reactions_dict=comment_reactions_dict,
                            post_reactions_dict=post_reactions_dict,
                            follower=follower_object
                            )


@posts.route("/delete/<post_public_id>")
@login_required
@verification_required
def delete_post(post_public_id):
    post = Post.query.filter_by(public_id=post_public_id).first_or_404()
    if post.author != current_user:
        abort(403)

    post_service = PostService(current_user)
    result = post_service.delete_post(post)

    if result is None:
        return redirect(url_for("posts.view_post", post_public_id=post.public_id))
    else:
        return redirect(url_for("main.home"))