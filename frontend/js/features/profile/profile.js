import { getProfile } from "../../api/profile.api.js";
import { renderProfile } from "../../components/profile.js";
import { handleGetPosts } from "../posts/post.js";
import {renderPosts} from "../../components/post.js"
import { renderNavPanel } from "../../components/navbar.js";

const mainPage = document.querySelector("#main-page")

export const handleGetMyProfile = async (userId) => {

    try {
        const response = await getProfile(userId);
        if (!response.success) {
        throw new Error(response.message);
        };

        const profile = renderProfile(response.data);
        const postsresponse = await handleGetPosts();
        const fragment = renderPosts(postsresponse.posts)
        
        mainPage.append(profile)
        
        const newSectionElement = document.createElement("section")
        newSectionElement.setAttribute("class", "container profile-posts-section")
        newSectionElement.append(fragment)
        mainPage.append(newSectionElement)
        mainPage.append(renderNavPanel())

    } catch (error) {
        throw (error);
    }
}