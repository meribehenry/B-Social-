import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js";
import { followState, setDOMFollowState } from "../follow/followState.js";


export const renderProfile = (profile) => {
    const template = document.querySelector("#profile-template");
    const profileTemplate = template.content.cloneNode(true);

    const profilePicture = profileTemplate.querySelector(".profile-pic")
    const firstname = profileTemplate.querySelector(".firstname")
    const lastname = profileTemplate.querySelector(".lastname")
    const username = profileTemplate.querySelector(".username")
    const followButton = profileTemplate.querySelector("[data-button]")
    const followingCount = profileTemplate.querySelector(".following-count")
    const followerscount = profileTemplate.querySelector(".followers-count")
    const bio = profileTemplate.querySelector(".bio")

    firstname.textContent = profile.firstname;
    lastname.textContent = profile.lastname;
    username.textContent = `@${profile.user.username}`;
    bio.textContent = profile.bio;
    followerscount.textContent = ` ${profile.user.num_of_followers} followers`
    followingCount.textContent = ` ${profile.user.num_of_following} following`
    followButton.dataset.userId = profile.user.public_id

    if (profile.profile_pic_url === "default.jpg") {
        profilePicture.src = "../../images/default.jpg";
    } else {
        profilePicture.src = profile.profile_pic_url; 
    };

    if (!authState.user) {
        retrieveCachedAuthenticated()
    }

    if (profile.user.public_id === authState?.user?.public_id ?? null) {
        followButton.innerHTML = "<p>Edit</p>"
        followButton.setAttribute("class", "btn btn-primary")
        followButton.class = "btn btn-primary"
        followButton.dataset.action = "edit"
            
    } else {
        setDOMFollowState(profile.user, followButton)
    }

    return profileTemplate;

};