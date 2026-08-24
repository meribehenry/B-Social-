
import { authState } from "../state/auth.state.js";
import {appState} from "../state/state.store.js"

const template = document.querySelector("#comment-template");


export const renderComment = (comment) => {
    console.log(comment)
    
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

    const cachedCommentsState = JSON.parse(localStorage.getItem("cachedCommentsState"));
    const likedCommentIds = new Set(cachedCommentsState.likedCommentIds);
    const dislikedCommentIds = new Set(cachedCommentsState.dislikedCommentIds);

    if (likedCommentIds.has(comment.public_id)) {
        likeIcon.src = "../../reaction/thumbs-up-solid.svg";
        likeIcon.setAttribute('data-reaction', "liked")
        dislikeIcon.src = "../../reaction/thumbs-down-outline.svg";
        dislikeIcon.setAttribute('data-reaction', "none")
    }; 

    if (dislikedCommentIds.has(comment.public_id)) {
        dislikeIcon.src = "../../reaction/thumbs-down-solid.svg";
        dislikeIcon.setAttribute('data-reaction', "disliked")
        likeIcon.src = "../../reaction/thumbs-up-outline.svg";
        likeIcon.setAttribute('data-reaction', "none")
        
    };

    if (!dislikedCommentIds.has(comment.public_id) && !likedCommentIds.has(comment.public_id)) {
        likeIcon.src = "../../reaction/thumbs-up-outline.svg";
        likeIcon.setAttribute('data-reaction', "none")
        dislikeIcon.src = "../../reaction/thumbs-down-outline.svg";
        dislikeIcon.setAttribute('data-reaction', "none")
    };

    if (comment.author.public_id !== authState.user?.public_id ?? null) {
        if (appState.followedUsers.has(comment.author.public_id)){
            followButton.textContent = "following";
            followButton.setAttribute("class", "btn btn-primary-outline")
        } else {
            followButton.textContent = "follow";
            followButton.setAttribute("class", "btn btn-primary")
        }
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