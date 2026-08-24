import { handleGetNotifications } from "../features/notifications/notification.js";

const mainPage = document.querySelector("#main-page");

export const initNotification = async () => {
    await handleGetNotifications(mainPage);
    
};