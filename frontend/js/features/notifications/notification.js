import { getNotifications, deleteNotifications, deleteNotification } from "../../api/notification.api.js";
import { renderNotifications } from "../../components/notification.js";

export const handleGetNotifications = async () => {
    
    const mainPage = document.querySelector("#main-page");
    const newSectionElement = document.createElement("section")
    newSectionElement.setAttribute("class", "container notifications-section")

    try {
        const response = await getNotifications ();
        if (!response.success) {
        throw new Error(response.message);
        };

        const apiNotifications = response.data.notifications;
        const fragment = renderNotifications(apiNotifications);

        newSectionElement.append(fragment)
        mainPage.append(newSectionElement)


    } catch (error) {
        throw (error);
    }
};


export const handleDeleteNotification =  async (notificationId) => {
    const response = await deleteNotification (notificationId);

    if (!response.ok) {
        throw (response);
    }

    return response.data;

};

export const handleDeleteNotifications =  async () => {
    const response = await  deleteNotifications ();

    if (!response.ok) {
        throw (response);
    }

    return response;

};
