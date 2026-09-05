import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js"
import { renderAppNavbar } from "../componets/navbars.js"
import { createPost } from "./api.js"
import { renderPost } from "./postDom.js"
import { saveState } from "../router/appRouter.js"
import { editPost } from "./api.js"


const title = document.querySelector("#title")
const body = document.querySelector("body")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")

export const renderNewPostPage = () => {
    
    history.pushState(
        {
            page: "new post",
        },
        "",
        `/app/post/create`
    );

    const newSectionElement = document.createElement("section");
    newSectionElement.setAttribute("class", "container new-post-container");
    const html = `
    <form id="new-post-form" action="">
        <label for="content" class="label">Content</label>
        <textarea name="content" id="content" placeholder="Type here...." class="new-post-text-area"></textarea>
        <input  id="post-file-input" name="files" class="post-file-input" type="file">
        <button id="create-post" type="submit">Create Post</button>
    </form>
    `
    newSectionElement.innerHTML = html

    header.innerHTML = "";
    mainPage.innerHTML = "";

    title.textContent = "create post"
    body.dataset.page = "create post"
    header.append(renderAppNavbar("Create post"))
    mainPage.append(newSectionElement)
    mainPage.addEventListener("submit", handleCreatePost)
}


export const handleCreatePost = async (event) => {
    event.preventDefault()

    const form = event.target.closest("form")
    const button = form.querySelector("#create-post");
    console.log(form)
    if (button.id !== "create-post") {
        return
    }
    const formData = new FormData(form);
    for (let pair of formData.entries()) {
        console.log(pair[0], pair[1])
    }

    try {
        const response = await createPost(formData);

        if (!response.success) {
            console.log(response.message)
        }
        
        // const firstPost = mainPage.querySelector(".post-article")
        // const feedSection = mainPage.querySelector(".feed-section")
        // const postsSection = mainPage.querySelector(".posts-section")
        // const newPost = renderPost(response.data)
        // feedSection?.insertBefore(newPost. firstPost)
        // postsSection?.insertBefore(newPost, firstPost)
        window.location.href = "/app"
        

    } catch (error) {
        console.log(error.message)

    }
};

export const renderEditPostPage = (postElement) => {
    const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };
    
    saveState(title.textContent, previousState)

    history.pushState(
        {
            page: "new post",
        },
        "",
        `/app/post/${postElement.dataset.postId}/edit`
    );

    const postContent = postElement.querySelector(".post-content")
    const postImage = postElement.querySelector(".post-media")

    let imageSrc = ""
    if (postImage?.src) {
        imageSrc = postImage.src
    }
    const newSectionElement = document.createElement("section");
    newSectionElement.setAttribute("class", "container edit-post-container");

    const html = `
    <form id="edit-post-form" action="" data-post-id="${postElement.dataset.postId}">
        <label for="content" class="label">Content</label>
        <textarea name="content" id="content class="edit-post-text-area">${postContent.textContent}</textarea>
        <img src="${imageSrc}"} alt="Post Media" class="edit-post-image">
        <button id="edit-post" type="submit">Edit</button>
    </form>
    `
    newSectionElement.innerHTML = html

    header.innerHTML = "";
    mainPage.innerHTML = "";

    title.textContent = "edit post"
    body.dataset.page = "edit post"
    header.append(renderAppNavbar("Edit post"))
    mainPage.append(newSectionElement)
    const button = newSectionElement.querySelector("#edit-post")
    button.addEventListener("click", handleEditPost)

}

export const handleEditPost = async (event) => {
    event.preventDefault()

    const form = event.target.closest("form")
    const button = form.querySelector("#edit-post");

    if (button.id !== "edit-post") {
        return null
    }


    const formData = new FormData(form);
    for (let pair of formData.entries()) {
        console.log(pair[0], pair[1])
    }

    try {
        const response = await editPost(formData, form.dataset.postId);

        if (!response.success) {
            console.log(response.message)
        }
        
        // const firstPost = mainPage.querySelector(".post-article")
        // const feedSection = mainPage.querySelector(".feed-section")
        // const postsSection = mainPage.querySelector(".posts-section")
        // const newPost = renderPost(response.data)
        // feedSection?.insertBefore(newPost. firstPost)
        // postsSection?.insertBefore(newPost, firstPost)
        window.location.href = "/app"
        
    } catch (error) {
        console.log(error.message)

    }
};
