import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js"
import { renderAppNavbar, navPanelEventListener, renderAppNavPanel } from "../componets/navbars.js"
import { createComment } from "./api.js"
import { saveState } from "../router/appRouter.js"


const title = document.querySelector("#title")
const body = document.querySelector("body")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")

export const renderNewCommentPage = (postId) => {
    const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };
    
    saveState(title.textContent, previousState)


    history.pushState(
        {
            page: "new comment",
        },
        "",
        `/app/post/${postId}/comment`
    );

    const newSectionElement = document.createElement("section");
    newSectionElement.setAttribute("class", "container new-comment-container");
    const html = `
    <form id="new-comment-form" action="">
        <label for="content" class="label">Content</label>
        <textarea type="text" name="content" id="content" placeholder="Type here...." class="new-comment-text-area"></textarea>
        <button id="create-comment" type="submit" data-post-id="${postId}">Comment</button>
    </form>
    `
    newSectionElement.innerHTML = html

    header.innerHTML = "";
    mainPage.innerHTML = "";

    title.textContent = "create comment"
    body.dataset.page = "create comment"
    header.append(renderAppNavbar("Create comment"))
    mainPage.append(newSectionElement)
    mainPage.addEventListener("click", handleCreateComment)
}


export const handleCreateComment = async (event) => {
    event.preventDefault()

    const button = event.target;
    const form = event.target.closest("form")

    if (button.id !== "create-comment") {
        return
    }
    const content = form.content.value.trim();
    const postId = button.dataset.postId
    console.log(content)

    try {
        const response = await createComment(postId, content);

        if (!response.success) {
            console.log(response.message)
        }
        

        window.location.href = `/app/post/${postId}`

    } catch (error) {
        console.log(error.message)

    }
};


export const renderEditCommentPage = (event) => {
    const commentElement = event.target.closest(".comment-article")
    const postElement = event.target.closest(".post-article")
    console.log(commentElement, postElement)

    if (!commentElement) {
        return null
    }

    const postID = postElement.dataset.postId
    const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };
    
    saveState(title.textContent, previousState)

    history.pushState(
        {
            page: "edit comment",
        },
        "",
        `/app/comment/${commentElement.dataset.commentId}/edit`
    );

    const commentContent = commentElement.querySelector(".comment-content")

    const newSectionElement = document.createElement("section");
    newSectionElement.setAttribute("class", "container edit-comment-container");


    const html = `
    <form id="edit-comment-form" action="" data-comment-id="${commentElement.dataset.commentId}">
        <label for="content" class="label">Content</label>
        <textarea type="text" name="content" id="content" class="edit-comment-text-area">${commentContent.textcontent}</textarea>
        <button id="edit-comment" type="submit" data-post-id="${postId}">Edit</button>
    </form>
    `
    newSectionElement.innerHTML = html

    header.innerHTML = "";
    mainPage.innerHTML = "";

    title.textContent = "edit comment"
    body.dataset.page = "edit comment"
    header.append(renderAppNavbar("Edit comment"))
    mainPage.append(newSectionElement)
    mainPage.addEventListener("click", handleEditComment)

}

export const handleEditComment = async (event) => {
    event.preventDefault()

    const form = event.target.closest("form")
    const button = form.querySelector("#edit-comment");

    if (button.id !== "edit-comment") {
        return null
    }


    const formData = new FormData(form);

    try {
        const response = await editComment(form.content.value.trim(), form.dataset.commentId);

        if (!response.success) {
            console.log(response.message)
        }
        

        window.location.href = `/app/post/${button.dataset.postId}`
        
    } catch (error) {
        console.log(error.message)

    }
};