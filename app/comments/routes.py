from flask import Blueprint, render_template, redirect, request, url_for, flash, abort
from app.likes.utils import like_comment, dislike_comment
from app.models import Post, Comment
from app.extensions import db
from .forms import CommentForm
from flask_login import login_required, current_user


comments= Blueprint("comments", __name__)


@comments.route("/post/<int:post_id>/new", methods=["GET", "POST"])
@login_required
def new_comment(post_id):
    post = Post.query.get_or_404(post_id)

    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post=post)

        post.num_of_comments = post.num_of_comments + 1

        try:
            db.session.add(comment)
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "danger")
            return redirect(url_for("comments.new_comment", post_id=post.id))
        
        flash("Comment sent successfully", "success")
        return redirect(url_for("posts.view_post", post_id=post.id))

    return render_template("comments/new_comment.html", form=form, title="New Comment")


@comments.route("/edit/<int:comment_id>", methods=["GET", "POST"])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.author != current_user:
        abort(403)

    form = CommentForm()

    if form.validate_on_submit():
            
        comment.content = form.content.data
        comment.edited = True

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}. Please try again", "danger")
            return redirect(url_for("comments.edit_comment", comment_id=comment.id))
        
        flash("Comment successfully edited", "success")
        return redirect(url_for("comments.view_comment", comment_id=comment.id))
    
    elif request.method == "GET":
        form.content.data = comment.content
    
    return render_template("comments/new_comment.html", form=form, title="Edit Comment")
        

@comments.route("/view/<int:comment_id>")
@login_required
def view_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    post_reaction = None
    if request.args.get("reaction", type=str):
        reaction = request.args.get("reaction", type=str)
        if reaction == "like":
            post_reaction = like_comment(comment, current_user)
        else:
            post_reaction = dislike_comment(comment, current_user)
        return redirect(url_for("comments.view_comment", comment_id=comment.id))
        
    return render_template("comments/view_comment.html", comment=comment, title="View Comment", post_reaction=post_reaction)


@comments.route("/delete/<int:comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post.id
    if comment.author != current_user:
        abort(403)

    try:
        db.session.delete(comment)
        post = Post.query.get(post_id)
        post.num_of_comments = post.num_of_comments - 1
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f"Error: {e}. Please try again", "danger")
        return redirect(url_for("comments.view_comment", comment_id=comment.id))
    
    flash("Comment successfully deleted", "success")
    return redirect(url_for("posts.view_post", post_id=post_id))