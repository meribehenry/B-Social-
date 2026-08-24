import { authState } from "../state/auth.state.js";
import { appState } from "../state/state.store.js";


export const renderSearchResult = (user) => {
    const template = document.querySelector("#search-template");
    const searchTemplate = template.content.cloneNode(true);
    
    const postArticle = searchTemplate.querySelector(".post-article");
    const firstname = searchTemplate.querySelector(".author-firstname");
    const lastname = searchTemplate.querySelector(".author-lastname");
    const username = searchTemplate.querySelector(".author-username");
    const profileImage = searchTemplate.querySelector("#author-profile-image");
    const followButton = searchTemplate.querySelector("[data-button=follow-button]")

    firstname.textContent = user.profile.firstname;
    lastname.textContent = userr.profile.lastname;
    username.textContent = `@${user.author.username}`;

    if (user.profile.profile_pic_url === "default.jpg") {
            profileImage.src = "../../images/default.jpg";
    } else {
        profileImage.src = user.profile.profile_pic_url; 
    }

    if (post.author.public_id !== authState.user?.public_id ?? null) {
        if (appState.followedUsers.has(post.author.public_id)){
            followButton.textContent = "following";
            followButton.setAttribute("class", "btn btn-primary-outline")
        } else {
            followButton.textContent = "follow";
            followButton.setAttribute("class", "btn btn-primary")
            }
    }

    return searchTemplate;
}