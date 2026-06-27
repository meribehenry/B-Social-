from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from app.models import Post, Comment
from .forms import CommentForm
from flask_login import login_required, current_user
from app.services.comment_service import CommentService
from app.services.reaction_service import ReactionService
from app.utils.decorators import verification_required
from app.utils.reaction_dict import get_user_comment_reactions_dict


comments= Blueprint("comments", __name__)


@comments.route("/post/<post_public_id>/new", methods=["GET", "POST"])
@login_required
@verification_required
def new_comment(post_public_id):
    post = Post.query.filter_by(public_id=post_public_id).first_or_404()

    form = CommentForm()

    if form.validate_on_submit():
        comment_service = CommentService(current_user)
        result = comment_service.create_comment(form, post)

        if result is None:
            return redirect(url_for("comments.new_comment", post_public_id=post.public_id))
        
        return redirect(url_for("posts.view_post", post_public_id=post.public_id))

    return render_template("comments/new_comment.html", form=form, title="New Comment")


@comments.route("/edit/<comment_public_id>", methods=["GET", "POST"])
@login_required
@verification_required
def edit_comment(comment_public_id):
    comment = Comment.query.filter_by(public_id=comment_public_id).first_or_404()
    if comment.author != current_user:
        abort(403)

    form = CommentForm()

    if form.validate_on_submit():
        comment_service = CommentService(current_user)
        result = comment_service.edit_comment(form, comment)
            
        if not result:
            return redirect(url_for("comments.edit_comment", comment_public_id=comment.public_id))
        
        return redirect(url_for("comments.view_comment", comment_public_id=comment.public_id))
    
    elif request.method == "GET":
        form.content.data = comment.content
    
    return render_template("comments/new_comment.html", form=form, title="Edit Comment")
        

@comments.route("/view/<comment_public_id>")
@login_required
@verification_required
def view_comment(comment_public_id):
    comment = Comment.query.filter_by(public_id=comment_public_id).first_or_404()

    post_reaction = None
    if request.args.get("reaction", type=str):
        reaction_service = ReactionService()
        reaction = request.args.get("reaction", type=str)
        if reaction == "like":
            post_reaction = reaction_service.like_comment(comment, current_user)
        else:
            post_reaction = reaction_service.dislike_comment(comment, current_user)
        return redirect(url_for("comments.view_comment", comment_public_id=comment.public_id))
    
    comment_reactions_dict =  get_user_comment_reactions_dict(current_user)
    return render_template("comments/view_comment.html", comment=comment, title="View Comment", post_reaction=post_reaction, comment_reactions_dict=comment_reactions_dict)


@comments.route("/delete/<comment_public_id>")
@login_required
@verification_required
def delete_comment(comment_public_id):
    comment = Comment.query.filter_by(public_id=comment_public_id).first_or_404()

    if comment.author != current_user:
        abort(403)

    comment_service = CommentService(current_user)
    post_public_id = comment_service.delete_comment(comment)

    if not post_public_id:
        return redirect(url_for("comments.view_comment", comment_public_id=comment.public_id))
    
    return redirect(url_for("posts.view_post", post_public_id=post_public_id))