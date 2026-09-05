import {renderAppNavbar, renderAppNavPanel, navPanelEventListener, appNavbarEventListener} from "../componets/navbars.js"
import { handlePostAction } from "../post/postAction.js";
import { renderPosts } from "../post/postDom.js";
import { saveState } from "../router/appRouter.js";
import { getUserSearchResult } from "./api.js";
import { renderSearchResult } from "./searchDom.js";
import { handleFollow } from "../follow/followAction.js";
import { getState } from "../router/appRouter.js";


export const handleGetUserSearchResult = async (event) => {
    event.preventDefault()
    const form = event.target.closest("form")
    const word = form.search.value.trim()
    const postsSection = document.querySelector(".search-results-section")

    history.pushState(
            {
                page: "search",
            },
            "",
            `/app/search/?search=${word}`
        );


    try {
        const response = await getUserSearchResult(word);
        if (!response.success) {
            throw new Error(response.message);
        };


        postsSection.innerHTML = ""
        if (!response.data.users || response.data.users.length===0) {
            postsSection.innerHTML = `<h4>No results for ${word}</h4>`
            return
        }

        for (const result of response.data.users) {
            console.log(result)
        if (result.posts.length!==0) {
            const posts = renderPosts(result.posts)
            postsSection.append(posts)
        } else {
            const user = renderSearchResult(result)
            postsSection.append(user)
        }
    }

    } catch (error) {
        throw (error);
    }
};

const body = document.querySelector("body")
const title = document.querySelector("title")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")



export const renderSearchPage = async (context) => {

    const previousState = {
            html: mainPage.innerHTML,
            scrollY: window.scrollY
        };
    
        saveState(title.textContent, previousState)
    
        history.pushState(
            {
                page: "search",
    
            },
            "",
            `/app/search`
        );

    if (context && Object.keys(context).length !== 0) {
            restoreSearchPage(context);
            return;
        }

    const postsSection= document.createElement("section")
    postsSection.setAttribute("class", "search-results-section")

    postsSection.innerHTML = "<h4>Make A Search</h4>"
    const navbar = renderAppNavbar("Search")
    const navbarImageContainer = navbar.querySelector(".app-navbar-image-container")
    const logo = navbar.querySelector(".logo-md")
    const formElement = document.createElement("form")
    formElement.setAttribute("class", "search-area")
    const searchBoxHTML = `
        <input class="search-box" type="text" placeholder="Search" name="search">
        <button class="search-submit-button" type="submit"><img class="search-icon" src="../svgs/search-outline.svg" alt="Search Icon"></button>
    `
    formElement.innerHTML = searchBoxHTML
    navbarImageContainer.insertBefore(formElement, logo)

    
    header.innerHTML = ""
    mainPage.innerHTML = ""
    title.textContent = "search"
    body.dataset.page = "search"
    header.append(navbar)
    mainPage.append(postsSection)
    mainPage.append(renderAppNavPanel("Search"))
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)
    const button = formElement.querySelector(".search-submit-button")
    button.addEventListener("click", handleGetUserSearchResult)
}

export const restoreSearchPage = (context) => {

    const retrivedValue = getState("search")

    if (!retrivedValue || Object.keys(retrivedValue).length === 0) {
        renderSearchPage(context={})
        return
    };

    const navbar = renderAppNavbar("Search")
    const logo = navbar.querySelector(".logo-md")
    const navbarImageContainer = navbar.querySelector(".app-navbar-image-container")
    const formElement = document.createElement("form")
    formElement.setAttribute("class", "search-area")
    const searchBoxHTML = `
        <input class="search-box" type="text" placeholder="Search" name="search">
        <button class="search-submit-button" type="submit"><img class="search-icon" src="../svgs/search-outline.svg" alt="Search Icon"></button>
    `
    formElement.innerHTML = searchBoxHTML
    navbarImageContainer.insertBefore(formElement, logo)

    header.innerHTML = ""
    mainPage.innerHTML = ""
    title.textContent = "search"
    body.dataset.page = "search"
    header.append(navbar)
    mainPage.innerHTML = retrivedValue.html
    // mainPage.append(renderAppNavPanel("Search"))
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("click", navPanelEventListener)
    mainPage.addEventListener("click", handleFollow)
    header.addEventListener("click", appNavbarEventListener)
    const button = formElement.querySelector(".search-submit-button")
    button.addEventListener("click", handleGetUserSearchResult)

    requestAnimationFrame(() => {
        window.scrollTo(0, retrivedValue.scrollY);
    })

};