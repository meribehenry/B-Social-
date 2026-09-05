import { renderHomePage } from "../home/page.js";
import { renderNotificationPage } from "../notification/page.js";
import { handleViewPost } from "../post/postAction.js";
import { renderSearchPage } from "../search/page.js";
import { renderProfilePage } from "../profile/page.js";
import { authState } from "../../auth/authState.js";
import { renderNewPostPage } from "../post/page.js";
import { renderNewCommentPage } from "../comments/page.js";


export const initAppRouter = () => {
    window.addEventListener("popstate", handlePopstate);

    handleAppRoute();

}

export const navigateTo = (path, state) => {
        history.pushState(
        state,
        "",
        path
    );

    handleAppRoute();
}

export const handlePopstate = (event) => {
    handleAppRoute(
        {
            fromHistoryNavigation: true,
            state: event.state
        }
    )
}

export const handleAppRoute = (context = {}) => {
    const path = window.location.pathname;

    if (path === "/app" || path === "/app/" || path === "/app/home"){
        renderHomePage(context);
        return;
    }

    if (path === "/app/search") {
        renderSearchPage(context)
        return;
    }

    if (path==="/app/post/create") {
        renderNewPostPage()
        return
    }

    if (path === "/app/notifications") {
        renderNotificationPage(context)
    }

    const postMatch = path.match(/^\/app\/post\/([a-zA-Z0-9-]+)$/);
    if (postMatch) {
        const postId = postMatch[1]
        handleViewPost(context, postId)
    }

    const postForCommentMatch = path.match(/^\/app\/post\/([a-zA-Z0-9-]+)\/comment$/);
    if (postForCommentMatch) {
        const postIdForComment = postForCommentMatch[1]
        renderNewCommentPage(postIdForComment)
    }

    const userMatch = path.match(/^\/app\/user\/([a-zA-Z0-9-]+)\/profile$/);
    if (userMatch) {
        const userId = userMatch[1]
        renderProfilePage(context, userId)
    }
}

const CACHE_PREFIX = "bsocial:page:"
export const saveState = (key, state) => {
    sessionStorage.setItem(
        `${CACHE_PREFIX}${key}`,
        JSON.stringify(state)
    );
};

export const getState = (key) => {
    const value = sessionStorage.getItem(
        `${CACHE_PREFIX}${key}`
    )

    return JSON.parse(value)
}

export const clearState = (key) => {
    const value = sessionStorage.removeItem(
        `${CACHE_PREFIX}${key}`
    )   
}

export const clearAllPagesState = () => {
    for (const key of Object.keys(sessionStorage)) {
        if (key.startsWith(CACHE_PREFIX)) {
            sessionStorage.removeItem(key)
        }
    }
}