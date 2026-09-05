import { authState, retrieveCachedAuthenticated } from "./authState.js";
import { renderAuthView } from "./authViews.js";


const checkAuth = () => {
    retrieveCachedAuthenticated()
    if (authState.token || authState.isAuthenticated===true) { 
        return true;
    } else {
        return false;
    }

}

export const startAuthApp = () => {
    const alreadyAuthentcated = checkAuth();
    
    if (alreadyAuthentcated) {
        window.location.href = "./app"
        return
    }

    const params = new URLSearchParams(window.location.search);

    const view = params.get("view") || "login";
    renderAuthView(view);

}

startAuthApp();