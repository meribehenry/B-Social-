import { getNotifications } from "./api.js";
import { saveState } from "../router/appRouter.js";
import { renderNotifications } from "./notificationDom.js";
import { renderAppNavbar, navPanelEventListener, appNavbarEventListener, renderAppNavPanel } from "../componets/navbars.js";


export const handleGetNotifications = async () => {
    try {
        const response = await getNotifications()

        if (!response.success) {
            console.log(response.message)
        }
        return response.data
    } catch (error) {
        console.log(error.message)
    }
};


const body = document.querySelector("body")
const title = document.querySelector("title")
const header = body.querySelector("#app-header")
const mainPage = body.querySelector("#app-main-page")


export const renderNotificationPage = async (context) => {

    const previousState = {
        html: mainPage.innerHTML,
        scrollY: window.scrollY
    };

    saveState(title.textContent, previousState)

    history.pushState(
        {
            page: "notifications",

        },
        "",
        `/app/notifications`
    );

    const data = await handleGetNotifications();
    const fragment = renderNotifications(data.notifications);

    const notificationSection = document.createElement("section")
    notificationSection.setAttribute("class", "container notifications-section")
    notificationSection.append(fragment);

    title.textContent = "notifications"
    body.dataset.page = "notifications"
    header.innerHTML = ""
    mainPage.innerHTML = ""

    header.append(renderAppNavbar("Notification"))
    mainPage.append(notificationSection);
    mainPage.append(renderAppNavPanel())
    mainPage.addEventListener("click", navPanelEventListener)
    header.addEventListener("click", appNavbarEventListener)
};