import { getState, saveState } from "../router/appRouter.js"
import { getPosts } from "../post/api.js"
import { navPanelEventListener, renderAppNavbar, appNavbarEventListener } from "../componets/navbars.js";
import { renderPosts } from "../post/postDom.js";
import { renderAppNavPanel } from "../componets/navbars.js";
import { handlePostAction } from "../post/postAction.js";
import { handlePostLikeReaction, handlePostDislikeReaction } from "../post/postReaction.js";
import { handleFollow } from "../follow/followAction.js";


export const handleGetFeed = async () => {
    try {
        const response = await getPosts()

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


export const renderHomePage = async (context) => {

    if (title) {
        const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };

        saveState(title.textContent, previousState)
    }

        history.pushState(
            {
                page: "home",

            },
            "",
            `/app`
        );

    if (context && Object.keys(context).length !== 0) {
        restoreHomePage(context);
        return;
    }

    const data = await handleGetFeed();
    const fragment = renderPosts(data.posts);

    const feedSection = document.createElement("section")
    feedSection.setAttribute("class", "container feed-section")
    feedSection.append(fragment);

    title.textContent = "home"
    body.dataset.page = "home"
    header.innerHTML = ""
    mainPage.innerHTML = ""

    header.append(renderAppNavbar("Home"))
    mainPage.append(feedSection);
    mainPage.append(renderAppNavPanel())
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)
};


export const restoreHomePage = (context) => {

    const retrivedValue = getState("home")

    if (!retrivedValue || Object.keys(retrivedValue).length === 0) {
        renderHomePage(context={})
        return
    };


    title.textContent = "home"
    body.dataset.page = "home"
    header.innerHTML = ""
    mainPage.innerHTML = ""
    header.append(renderAppNavbar("Home"))
    mainPage.innerHTML = retrivedValue.html
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)
    // const navIcon = header.querySelectorAll(".app-nav-icon")
    // navIcon.addEventListener("click", appNavbarEventListener)

    requestAnimationFrame(() => {
        window.scrollTo(0, retrivedValue.scrollY);
    })

};