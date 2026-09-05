import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js";
import { postsState, retrieveCachedPostsState } from "./postsState.js";
import { setFollowState, retrievecachedFollowState, setDOMFollowState } from "../follow/followState.js";


export const thumbsUpSolid = "../../../svgs/reaction/thumbs-up-solid.svg"
export const thumbsUpOutline= "../../../svgs/reaction/thumbs-up-outline.svg"
export const thumbsDownSolid = "../../../svgs/reaction/thumbs-down-solid.svg"
export const thumbsDownOutline = "../../../svgs/reaction/thumbs-down-outline.svg"



export const renderPost = (post) => {
    const template = document.querySelector("#post-template");
    
    const postTemplate = template.content.cloneNode(true);

    const postArticle = postTemplate.querySelector(".post-article");
    const firstname = postTemplate.querySelector(".author-firstname");
    const lastname = postTemplate.querySelector(".author-lastname");
    const username = postTemplate.querySelector(".author-username");
    const profileImage = postTemplate.querySelector("#author-profile-image");
    const postContent = postTemplate.querySelector(".post-content");
    const postMediaContainer = postTemplate.querySelector(".post-media-container");
    const likeCount = postTemplate.querySelector(".like-count");
    const commentCount = postTemplate.querySelector(".comment-count");
    const clicksCount = postTemplate.querySelector(".clicks-count");
    const likeIcon = postTemplate.querySelector(".like-icon");
    const dislikeIcon = postTemplate.querySelector(".dislike-icon");
    const followButton = postTemplate.querySelector("[data-button=follow-button]")

    firstname.textContent = post.author.profile.firstname;
    lastname.textContent = post.author.profile.lastname;
    username.textContent = `@${post.author.username}`;
    if (post.author.profile.profile_pic_url === "default.jpg") {
            profileImage.src = "../../../images/default.jpg";
    } else {
        profileImage.src = post.author.profile.profile_pic_url; 
    }
    postContent.textContent = post.content;
    likeCount.textContent = post.num_of_likes
    commentCount.textContent = post.num_of_comments
    clicksCount.textContent = post.num_of_clicks
    postArticle.dataset.postId = post.public_id;
    followButton.dataset.userId = post.author.public_id
    
    if (!postsState.likedPostIds || !postsState.dislikedPostIds) {
        retrieveCachedPostsState()
    }

    const likedPostIds = postsState.likedPostIds
    const dislikedPostIds = postsState.dislikedPostIds

    if (likedPostIds.has(post.public_id)) {
        likeIcon.src = thumbsUpSolid;
        likeIcon.setAttribute('data-reaction', "liked")
        dislikeIcon.src = thumbsDownOutline;
        dislikeIcon.setAttribute('data-reaction', "none")
    };

    if (dislikedPostIds.has(post.public_id)) {
        dislikeIcon.src = thumbsDownSolid;
        dislikeIcon.setAttribute('data-reaction', "disliked")
        likeIcon.src = thumbsUpOutline;
        likeIcon.setAttribute('data-reaction', "none")
        
    };

    if (!dislikedPostIds.has(post.public_id) && !likedPostIds.has(post.public_id)) {
        likeIcon.src = thumbsUpOutline;
        likeIcon.setAttribute('data-reaction', "none")
        dislikeIcon.src = thumbsDownOutline;
        dislikeIcon.setAttribute('data-reaction', "none")
    };

    if (!authState.user) {
        retrieveCachedAuthenticated()
    }

    if (post.author.public_id !== authState?.user?.public_id ?? null) {
        setDOMFollowState(post.author, followButton)
    }

    let count = 1;
    for (const media of post.medias) {
        
        if (media.media_type === "photo"){
            const newImgElement = document.createElement("img");
            newImgElement.setAttribute("src", media.file_url);
            newImgElement.setAttribute("class", `post-media post-media-${media.media_type}`);
            newImgElement.setAttribute("alt", `Post Image ${count}`);
            postMediaContainer.append(newImgElement);
        } else {
            const newVideoElement = document.createElement("video");
            newVideoElement.setAttribute("src", media.file_url);
            newVideoElement.setAttribute("class", `post-media post-media-${media.media_type}`);
            newVideoElement.setAttribute("alt", `Post Video ${count}`);
            postMediaContainer.append(newVideoElement);
        };
        count += 1;
    }

    return postTemplate;

}

export const renderPosts = (posts) => {
    const fragment = document.createDocumentFragment();
    
    for (const post of posts) {
        const htmlPost = renderPost(post)
        fragment.append(htmlPost);  
    }

    return fragment;
};

export const removePost = (post) => {
    posts = document.querySelector("#home")
    postToRemove = posts.querySelector(`[post-id=${post.public_id}]`);

    if (postToRemove){
        posts.remove(postToRemove);
    };

    return posts;
}