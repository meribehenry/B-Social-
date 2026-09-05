import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js";
import { setDOMFollowState } from "../follow/followState.js";


export const renderComment = (comment) => {
    
    const template = document.querySelector("#comment-template");
    
    const commentTemplate = template.content.cloneNode(true);

    const commentArticle = commentTemplate.querySelector(".comment-article");
    const firstname = commentTemplate.querySelector(".author-firstname");
    const lastname = commentTemplate.querySelector(".author-lastname");
    const username = commentTemplate.querySelector(".author-username");
    const profileImage = commentTemplate.querySelector("#author-profile-image");
    const commentContent = commentTemplate.querySelector(".comment-content");
    const likeCount = commentTemplate.querySelector(".like-count");
    const likeIcon = commentTemplate.querySelector(".like-icon");
    const dislikeIcon = commentTemplate.querySelector(".dislike-icon");
    const followButton = commentTemplate.querySelector("[data-button]")

    firstname.textContent = comment.author.profile.firstname;
    lastname.textContent = comment.author.profile.lastname;
    username.textContent = `@${comment.author.username}`;
    if (comment.author.profile.profile_pic_url === "default.jpg") {
            profileImage.src = "../../images/default.jpg";
    } else {
        profileImage.src = comment.author.profile.profile_pic_url; 
    }
    commentContent.textContent = comment.content;
    likeCount.textContent = comment.num_of_likes
    commentArticle.dataset.commentId = comment.public_id;
    followButton.dataset.userId = comment.author.public_id

    const cachedCommentsState = JSON.parse(localStorage.getItem("cachedCommentsState"));
    const likedCommentIds = new Set(cachedCommentsState?.likedCommentIds);
    const dislikedCommentIds = new Set(cachedCommentsState?.dislikedCommentIds);

    if (likedCommentIds.has(comment.public_id)) {
        likeIcon.src = "../../svgs/reaction/thumbs-up-solid.svg";
        likeIcon.setAttribute('data-reaction', "liked")
        dislikeIcon.src = "../../svgs/reaction/thumbs-down-outline.svg";
        dislikeIcon.setAttribute('data-reaction', "none")
    }; 

    if (dislikedCommentIds.has(comment.public_id)) {
        dislikeIcon.src = "../../svgs/reaction/thumbs-down-solid.svg";
        dislikeIcon.setAttribute('data-reaction', "disliked")
        likeIcon.src = "../../svgs/reaction/thumbs-up-outline.svg";
        likeIcon.setAttribute('data-reaction', "none")
        
    };

    if (!dislikedCommentIds.has(comment.public_id) && !likedCommentIds.has(comment.public_id)) {
        likeIcon.src = "../../svgs/reaction/thumbs-up-outline.svg";
        likeIcon.setAttribute('data-reaction', "none")
        dislikeIcon.src = "../../svgs/reaction/thumbs-down-outline.svg";
        dislikeIcon.setAttribute('data-reaction', "none")
    };

    if (!authState.user) {
        retrieveCachedAuthenticated()
    }

    if (comment.author.public_id !== authState?.user?.public_id) {
        setDOMFollowState(comment.author, followButton)
    }

    return commentTemplate;
}


export const renderComments = (comments) => {
    const fragment = document.createDocumentFragment();
    for (const comment of comments) {
        fragment.append(renderComment(comment));
    }

    return fragment;
};

export const removeComment = (commentPublicId) => {
    comments = document.querySelector("#home")
    commentToRemove = comment.querySelector(`[comment-id=${commentPublicIid}]`);

    if (commentToRemove){
        comments.remove(commentToRemove);
    };

    return comments;
}