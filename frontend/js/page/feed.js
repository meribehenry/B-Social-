import { handleFeed} from "../features/feed/feed.js";
import { handlePostAction } from "../features/posts/post-action.js";
import { renderNavPanel } from "../components/navbar.js";

const mainPage = document.querySelector("#main-page");

export const initHome = () => {
    handleFeed();
    mainPage.addEventListener("click", handlePostAction);
    
};