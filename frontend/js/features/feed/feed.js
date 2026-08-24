import { renderPosts } from "../../components/post.js"
import { handleGetPosts } from "../posts/post.js"
import { renderNavPanel } from "../../components/navbar.js";

const main = document.querySelector("#main-page");
const feed = document.createElement("section");
feed.setAttribute("class", "container feed")
feed.setAttribute("id", "feed");

export const handleFeed = async () => {
    const data = await handleGetPosts();

    const fragment = renderPosts(data.posts);
    feed.append(fragment);
    main.append(feed);
    main.append(renderNavPanel())
};