// app.js
// The bootstrapper. Not where the app "lives" — just gets things started in order.

import { authState, setAuthenticated } from "./state/auth.state.js";
import { apiRequest } from "./api/client.js";
import {initLogin} from './page/login.js';
import {initRegister} from "./page/register.js"
import { initHome } from "./page/feed.js";
import { handleGetPostReactionsList } from "./features/reaction/post.reaction.js";
import { handleGetCommentReactionsList } from "./features/reaction/comment-reaction.js";
import { initNotification } from "./page/notification.js";
import { initMyProfile } from "./page/profile.js";
import { initSearch } from "./page/page.js";

export const loadTemplates = async () => {
  const res = await fetch('./templates.html'); // 1. Get the file
  const html = await res.text(); // 2. Turn it into a string
 
  const div = document.createElement('div'); // 3. Make a temp container
  div.innerHTML = html; // 4. Browser parses the string into real DOM nodes
 
  document.body.append(...div.children); // 5. Move all <template> into the real DOM
}


const startApp = async () => {

  handleGetPostReactionsList()
  handleGetCommentReactionsList()
  loadTemplates()

  const page = document.body.dataset.page;
  console.log("app initialized. page:", page, "authenticated:", authState.isAuthenticated);

  switch (page) {

      case "login":
          initLogin();
          break;
      
      case "register":
          initRegister();
          break;
      
      case "home":
          initHome();
          break;

      case "notification":
          initNotification();
          break
      
      case "profile":
          initMyProfile();
          break
      
      case "search":
          initSearch();
          break

      default:
          console.warn("Unknown Page:", page);
  }


}

startApp();