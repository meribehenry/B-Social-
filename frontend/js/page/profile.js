import { handleGetMyProfile } from "../features/profile/profile.js";
import { handlePostAction } from "../features/posts/post-action.js";

const mainPage = document.querySelector("#main-page");

export const initMyProfile = async () => {
    await handleGetMyProfile("65621469-6257-42bc-a7e0-4c45be8cd662");
    mainPage.addEventListener("click", handlePostAction)
}