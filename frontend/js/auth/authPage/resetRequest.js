import { resetRequest, verifyEmail } from "../authApi.js"

const authApp = document.querySelector("#auth-app")

export const renderResetRequestPage = () => {
    const title = document.querySelector("#title")
    const body= document.querySelector("body")

    title.textContent = "Reset Password Request"
    body.dataset.page = "reset-request";

    const html = `
    <form id="reset-request-form" action="" method="PATCH">

        <label for="reset-request">Email</label>
        <input id="reset-request" type="email" name="email" >

        <button id="send" type="submit">Send</button>
    </form>
    `
    authApp.innerHTML = "";
    authApp.innerHTML = html;

    resetRequestEventListener()
  }


export const handleResetRequest= async (event) => {
    event.preventDefault();

    const form = event.target;
    const email = form.email.value.trim();


  try {
    const response = await resetRequest(email);
    if (!response.success) {
        console.log(response.message)
    }

    console.log("Reset Password Link Sent")
    window.location.assign("/auth"); 

  } catch (error) {
    console.log(error)
  }
};


export const resetRequestEventListener = async () => {
    const form = document.querySelector("#reset-request-form");
    form.addEventListener("submit", handleResetRequest)
};
