import { authState } from "../state/auth.state.js";
import { appState } from "../state/state.store.js";


export const renderProfile = (profile) => {
    const template = document.querySelector("#profile-template");
    const profileTemplate = template.content.cloneNode(true);
    console.log("PP")
    console.log(profileTemplate)

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

    console.log(profileTemplate)
    if (profile.profile_pic_url === "default.jpg") {
            profilePicture.src = "../../images/default.jpg";
    } else {
        profilePicture.src = profile.profile_pic_url; 
    };

    if (profile.user.public_id !== authState.user?.public_id ?? null) {
            if (appState.followedUsers.has(profile.user.public_id)){
                followButton.textContent = "following";
                followButton.setAttribute("class", "btn btn-primary-outline")
            } else {
                followButton.textContent = "follow";
                followButton.setAttribute("class", "btn btn-primary")
            }
    };

    console.log(profileTemplate)

    return profileTemplate;

};