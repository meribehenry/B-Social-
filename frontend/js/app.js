// app.js
// The bootstrapper. Not where the app "lives" — just gets things started in order.

import { authState, setAuthenticated } from "./state/auth.state.js";
import { apiRequest } from "./api/client.js";
import {initLogin} from './page/login.js';
import {initRegister} from "./page/register.js"


const restoreSession= async () => {
    try {
      // If a refresh cookie exists, this returns a fresh access token.
      const data = await apiRequest("/auth/refresh", { method: "POST" });
      setAuthenticated(data.user, data.access_token);
      window.location.href = "./index.html";

    } catch {
      console.log("Pop")
      // No valid session — that's fine, user is just logged out.
    } finally {
      authState.initialized = true;
    }
};

// async function startApp() {
//   await restoreSession();

//   const page = document.body.dataset.page;
//   console.log("app initialized. page:", page, "authenticated:", authState.isAuthenticated);

//   // Later: route to page-specific init (initHome(), initProfile(), etc.)
//   // based on `page`, and redirect to /login if a protected page requires auth.
// }

// startApp();

const startApp = async () => {
  // await restoreSession();

  const page = document.body.dataset.page;
  console.log("app initialized. page:", page, "authenticated:", authState.isAuthenticated);
  console.log("here");

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

      default:
          console.warn("Unknown Page:", page);
  }
}
console.log("here");
startApp();