import { renderComments } from "../../components/comment.js";
import { handleGetComments } from "./comment.js"

export const handleViewComments = async (postElement) =>{
    const mainPage = document.querySelector("#main-page")
    const newSectionElement1 = document.createElement("section");
    newSectionElement1.setAttribute("class", "container view-comments-container");
    newSectionElement1.append(postElement);

    const newDivElement = document.createElement("div");
    newDivElement.setAttribute("class", "comments-section");

    const newHeadingElement = document.createElement("h5");
    newHeadingElement.setAttribute("class", "comments-section-heading")
    newHeadingElement.textContent = "Comments"
    newDivElement.append(newHeadingElement)
    
    const postId = postElement.dataset.postId;

    const comments = await handleGetComments(postId);
    const fragment = renderComments(comments)
    newDivElement.append(fragment)
    newSectionElement1.append(newDivElement)
    
    mainPage.innerHTML = "";
    const newSectionElement2 = document.createElement("section")
    newSectionElement2.setAttribute("class", "container");
    newSectionElement2.innerHTML = `
    <div class="view-comments-upper-part">
        <img class="menu" src="../../../images/default.jpg" alt="">
        <img class="logo-md" src="../../../images/logo.png" alt="Logo">
    </div>
    `

    mainPage.append(newSectionElement2);
    mainPage.append(newSectionElement1);
    
};