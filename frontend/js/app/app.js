import { initAppRouter } from "./router/appRouter.js"
import { authState, retrieveCachedAuthenticated, } from "../auth/authState.js";
import { handleGetPostReactionsList } from "./post/postReaction.js";
import { handleGetFollowingsList } from "./follow/followAction.js";

export const loadTemplates = async () => {
  const res = await fetch('/templates'); // 1. Get the file
  const html = await res.text(); // 2. Turn it into a string
 
  const div = document.createElement('div'); // 3. Make a temp container
  div.innerHTML = html; // 4. Browser parses the string into real DOM nodes
 
  document.body.append(...div.children); // 5. Move all <template> into the real DOM
}

const setAuth = () => {
    retrieveCachedAuthenticated()
    if (!authState || Object.keys(authState).length===0 || !authState.user) {
      
    window.location.href = "/auth?view=login"    
    }

}

const startApp = () => {
    setAuth()
    handleGetPostReactionsList()
    handleGetFollowingsList()
    loadTemplates()
    initAppRouter()
}

startApp()