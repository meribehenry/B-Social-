import { authState } from "../../auth/authState.js";
import { setDOMFollowState } from "../follow/followState.js";


const appState = {

}
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
    lastname.textContent = user.profile.lastname;
    username.textContent = `@${user.username}`;
    followButton.dataset.userId = user.public_id

    if (user.profile.profile_pic_url === "default.jpg") {
            profileImage.src = "/images/default.jpg";
    } else {
        profileImage.src = user.profile.profile_pic_url; 
    }

    if (user?.public_id !== authState?.user?.public_id ?? null) {
        setDOMFollowState(user)
    }

    return searchTemplate;
}