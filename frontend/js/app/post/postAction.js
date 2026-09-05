import { handlePostDislikeReaction, handlePostLikeReaction } from "./postReaction.js"
import { getPost } from "./api.js";
import { renderPost } from "./postDom.js";
import { getComments } from "../comments/api.js";
import { renderComments } from "../comments/commentDom.js";
import { renderAppNavbar, renderAppNavPanel, navPanelEventListener } from "../componets/navbars.js";
import { getState, saveState } from "../router/appRouter.js";
import { appNavbarEventListener } from "../componets/navbars.js";
import { handleFollow } from "../follow/followAction.js";
import { handleEditComment, renderNewCommentPage } from "../comments/page.js";
import { renderEditCommentPage } from "../comments/page.js";
import { renderEditPostPage } from "./page.js";


export const handlePostAction = async (event) => {
    event.preventDefault()
    const button = event.target.closest("button")
    const link = event.target.closest("a")
    console.log(link)

    const actions = new Set(["like", "dislike", "comment"])

    if (!button && !link) {
        return null;
    }

    if (button && !actions.has(button.dataset.action)) {
        return null
    }

    const postElement = event.target.closest(".post-article")
    const postId = postElement.dataset.postId
    console.log(postElement)

    
    
    if (button) {
        const action = button.dataset.action;
    
        if (action === "like") {
            await handlePostLikeReaction(postElement);
        };

        if (action === "dislike") {
            await handlePostDislikeReaction(postElement);
        };

        if (action === "comment") {
            await handleViewPost({}, postId)
        }
    }

    if (link) {
        const action = link.id;
        renderEditPostPage(postElement)
    }
}

const title = document.querySelector("#title")
const body = document.querySelector("body")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")

export const handleViewPost = async (context, postId) =>{

    const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };
    
    saveState(title.textContent, previousState)


    history.pushState(
        {
            page: "view post",
        },
        "",
        `/app/post/${postId}`
    );

    if (context && Object.keys(context).length !== 0) {
            handleRestoreViewPost(context);
            return;
        }

    const newSectionElement1 = document.createElement("section");
    newSectionElement1.setAttribute("class", "container view-post-container");
    const response = await getPost(postId);
    const postElement = renderPost(response.data)
    newSectionElement1.append(postElement);

    const newDivElement = document.createElement("div");
    newDivElement.setAttribute("class", "comments-section");

    // const newHeadingElement = document.createElement("h5");
    // newHeadingElement.setAttribute("class", "comments-section-heading")
    // newHeadingElement.textContent = "Comments"
    // newDivElement.append(newHeadingElement)
    // const newImg = document.createElement("img")
    // newImg.setAttribute("class", "comments-section-icon")
    const html = `
    <div class="comment-section-header">
        <h5 class="comments-section-heading">Comments</h5>
        <img class="comment-section-icon" src="/svgs/add-outline.svg">
    <div>
    `
    newDivElement.innerHTML = html
    console.log(newDivElement)
    
    try {

        const commentResponse = await getComments(postId);
        if (!commentResponse.success) {
            console.log(commentResponse.message);
        };
        const fragment = renderComments(commentResponse.data.comments)
        newDivElement.append(fragment)
        newSectionElement1.append(newDivElement)
            
    } catch (error) {
        console.log(error) ;     
    };


    header.innerHTML = "";
    mainPage.innerHTML = "";

    title.textContent = "view post"
    header.append(renderAppNavbar("View Post"))
    mainPage.append(newSectionElement1);
    mainPage.append(renderAppNavPanel())
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)
    const Icon = newDivElement.querySelector(".comment-section-icon")
    Icon.addEventListener("click", (event) => {
            event.preventDefault()
            renderNewCommentPage(postId)
        } )  
    mainPage.addEventListener("click", renderEditCommentPage)
    
};


export const handleRestoreViewPost = (context, postId) => {
    
        const retrivedValue = getState("view post")
    
        if (!retrivedValue || Object.keys(retrivedValue).length === 0) {
            handleViewPost(context={}, postId)
            return
        };

        header.innerHTML = ""
        mainPage.innerHTML = ""
        title.textContent = "view post"
        body.dataset.page = "view post"
        header.append(renderAppNavbar("View Post"))
        mainPage.innerHTML = retrivedValue.html
        mainPage.addEventListener("click", navPanelEventListener)
        mainPage.addEventListener("click", handleFollow)
        mainPage.addEventListener("click", handleEditComment)
        header.addEventListener("click", appNavbarEventListener)
        const Icon = newDivElement.querySelector(".comment-section-icon")
        Icon.addEventListener("click", (event) => {
            event.preventDefault()
            renderNewCommentPage(postId)
        }
    ) 
    
        requestAnimationFrame(() => {
            window.scrollTo(0, retrivedValue.scrollY);
        })

}