

export const renderNotification = (notification) => {
    const template = document.querySelector("#notification-template");

    const notificationTemplate = template.content.cloneNode(true);
    const actorProfilePic = notificationTemplate.querySelector(".actor-profile-pic");
    const actorFirstname = notificationTemplate.querySelector(".firstname");
    const actorSecondname = notificationTemplate.querySelector(".lastname");
    const notificationMessage = notificationTemplate.querySelector(".message");
    const notificationIcon = notificationTemplate.querySelector(".icon");

    if (notification.actor.profile.profile_pic_url === "default.jpg") {
        actorProfilePic.src = "../../images/default.jpg";
    } else {
        actorProfilePic.src = notification.actor.profile.profile_pic_url; 
    }
    actorFirstname.textContent =  notification.actor.profile.firstname;
    actorSecondname.textContent = notification.actor.profile.lastname;
    notificationMessage.textContent = notification.content;
    // notificationIcon.src = ""


    return notificationTemplate;

}

export const renderNotifications = (notifications) => {
    const fragment = document.createDocumentFragment();
    
    for (const notification of notifications) {
        const result = renderNotification(notification);
        fragment.append(result);  
    }

    return fragment;
};