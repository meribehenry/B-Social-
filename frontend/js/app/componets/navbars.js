import { renderHomePage } from "../home/page.js";
import { renderNotificationPage } from "../notification/page.js";
import { renderSearchPage } from "../search/page.js";
import { authState, retrieveCachedAuthenticated } from "../../auth/authState.js";
import { renderProfilePage } from "../profile/page.js";
import { renderNewPostPage } from "../post/page.js";


export const renderAppNavPanel = () => {
    const newDivElement = document.createElement("div");
    const newDivElement2 = document.createElement("div");
    newDivElement.setAttribute("class", "nav-panel");  
    newDivElement2.setAttribute("class", "nav-panel-container");  
    const html = `
        <img id="home" class="app-nav-panel-icon nav-current" src="/svgs/home-outline.svg" alt="Home">
        <img id="search" class="app-nav-panel-icon" src="/svgs/search-outline.svg" alt="Search">
        <div class="new-post-app-nav-panel-icon-container">
            <img id="new-post" class="app-nav-panel-icon" src="/svgs/add-outline-white.svg" alt="New Post">
        </div>
        <img id="notification" class="app-nav-panel-icon" src="/svgs/notifications-outline-black.svg" alt="Notification">
        <img id="profile" class="app-nav-panel-icon" src="/svgs/person-circle-outline.svg" alt="Profile">
    `
    newDivElement.innerHTML = html;
    newDivElement2.append(newDivElement)
    return newDivElement2;
};


export const renderAppNavbar = (page) => {
    let html = null;

    if (!authState.user) {
        retrieveCachedAuthenticated()
    }

    let imageSrc = "/images/default.jpg"
    if (authState.user.profile.profile_pic_url !== "default.jpg") {
        imageSrc = authState.user.profile.profile_pic_url
    }

    if (page==="Home") {
        html = `
            <div class="app-navbar-image-container">
                <h4>${page}</h4>
                <img class="logo-md" src="../images/logo.png" alt="Logo" > 
            </div> 
            <button class="home-offcanvas" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasExample" aria-controls="offcanvasExample">
                <img id="home-offcanvas"  class="navbar-${page}" src=${imageSrc} alt="" >
            </button>
            

            <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasExample" aria-labelledby="offcanvasExampleLabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasExampleLabel">Offcanvas</h5>
                    <img
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <div>
                        <p class="offcanvas-text">Feedback</p>
                        <p class="offcanvas-text">Logout</p>
                    </div>
                </div>
            </div> 

        `
        
    } else {
        html = `
            <div class="app-navbar-image-container">
                <h4>${page}</h4>
                <img class="logo-md" src="/images/logo.png" alt="Logo">   
            </div>
            <img  id="app-navbar-icon" class="navbar-back" src="/svgs/arrow-back-solid.svg" alt="" data-action="back">
        `
    }

    const newSectionElement = document.createElement("section");
    newSectionElement.setAttribute("class", "container app-navbar"); 
    newSectionElement.innerHTML = html
    return newSectionElement
}



// -------------- EVENT LISTENER -----------------
export const navPanelEventListener = (event) => {
    const appNavPanelICon = event.target.closest(".app-nav-panel-icon")
    console.log(appNavPanelICon)
    if (!appNavPanelICon) {
        return null;
    }

    if (appNavPanelICon.id === "home") {
        renderHomePage()
    }

    if (appNavPanelICon.id === "search") {
        renderSearchPage()
    }

    if (appNavPanelICon.id === "notification") {
        renderNotificationPage()
    }

    if (appNavPanelICon.id === "profile") {
        let userID = authState.user.public_id
        if (!userID) {
            const cachedAuthState = sessionStorage.getItem("cachedAuthenticated")
            userID = cachedAuthState?.user?.public_id
            if (!userID) {
                console.log("User not found")
            }
        }
        renderProfilePage({}, userID)
    }

    if (appNavPanelICon.id === "new-post") {
        renderNewPostPage()
    }
} 

export const appNavbarEventListener = (event) => {
    const appNavbarICon = event.target.closest("#app-navbar-icon")
    console.log(appNavbarICon)

    if (!appNavbarICon) {
        console.log("Returned Null")
        return null;
    }

    if (appNavbarICon.dataset.action==="offcanvas") {
        console.log("What")
        // To be determined
    } 

    if (appNavbarICon.dataset.action ==="back") {
        console.log("Backed")
        history.back()
    }


} 