import { handleGetUserSearchResult } from "../features/search/search.js";
import { handlePostAction } from "../features/posts/post-action.js";

const mainPage = document.querySelector("#main-page");

export const initSearch = () => {
    mainPage.addEventListener("click", handlePostAction)
    mainPage.addEventListener("submit", handleGetUserSearchResult)
}