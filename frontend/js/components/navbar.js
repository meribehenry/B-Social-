

export const renderNavPanel = () => {
    const newDivElement = document.createElement("div");
    const newDivElement2 = document.createElement("div");
    newDivElement.setAttribute("class", "nav-panel");  
    newDivElement2.setAttribute("class", "nav-panel-container");  
    const html = `
        <img class="nav-icon nav-current" src="../svgs/home-outline.svg" alt="Home">
        <img class="nav-icon" src="../svgs/search-outline.svg" alt="Search">
        <div class="new-post-nav-icon-container">
            <img class="nav-icon" src="../svgs/add-outline-white.svg" alt="New Post">
        </div>
        <img class="nav-icon" src="../svgs/notifications-outline-black.svg" alt="Notification">
        <img class="nav-icon" src="../svgs/person-circle-outline.svg" alt="Profile">
    `
    newDivElement.innerHTML = html;
    newDivElement2.append(newDivElement)
    return newDivElement2;

};