import { getState, saveState } from "../router/appRouter.js"
import { getPosts } from "../post/api.js"
import { navPanelEventListener, renderAppNavbar, appNavbarEventListener } from "../componets/navbars.js";
import { renderPosts } from "../post/postDom.js";
import { renderAppNavPanel } from "../componets/navbars.js";
import { handlePostAction } from "../post/postAction.js";
import { handlePostLikeReaction, handlePostDislikeReaction } from "../post/postReaction.js";
import { getProfile } from "./api.js";
import { renderProfile } from "./profileDom.js";
import { handleFollow } from "../follow/followAction.js";



export const handleGetProfile = async (userID) => {
    try {
        const response = await getProfile(userID)

        if (!response.success) {
            console.log(response.message)
        }
        return response.data
    } catch (error) {
        console.log(error.message)
    }
};


const body = document.querySelector("body")
const title = document.querySelector("title")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")


export const renderProfilePage = async (context, userID) => {

    const previousState = {
        html: mainPage.innerHTML,
        scrollY: window.scrollY
    };

    saveState(title.textContent, previousState)

    history.pushState(
        {
            page: "profile",

        },
        "",
        `/app/user/${userID}/profile`
    );

    if (context && Object.keys(context).length !== 0) {
        restoreProfilePage(context, userID);
        return;
    }

    const profile = await handleGetProfile(userID);
    const profileSection = renderProfile(profile)

    const postsSection = document.createElement("section")
    postsSection.setAttribute("class", "container posts-section")
    try {
        const response = await getPosts({user_public_id: userID});
        if (!response.success) {
            console.log(response.message)
        }

        const fragment = renderPosts(response.data.posts);
        postsSection.append(fragment);

    } catch (error) {
        console.log("An error occured", error)
    }
    

    title.textContent = "profile"
    body.dataset.page = "profile"
    header.innerHTML = ""
    mainPage.innerHTML = ""

    header.append(renderAppNavbar("Profile"))
    mainPage.append(profileSection)
    mainPage.append(postsSection);
    mainPage.append(renderAppNavPanel("Profile"))
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    header.addEventListener("click", appNavbarEventListener)
};


export const restoreProfilePage = (context, userID) => {

    const retrivedValue = getState("profile")

    if (!retrivedValue || Object.keys(retrivedValue).length === 0) {
        renderProfilePage({}, userID)
        return
    };

    title.textContent = "profile"
    body.dataset.page = "profile"
    header.innerHTML = ""
    mainPage.innerHTML = ""
    header.append(renderAppNavbar("Profile"))
    mainPage.innerHTML = retrivedValue.html
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)

    requestAnimationFrame(() => {
        window.scrollTo(0, retrivedValue.scrollY);
    })

};