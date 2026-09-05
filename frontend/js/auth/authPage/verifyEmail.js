import { verifyEmail } from "../authApi.js"
import {handleResendOtp} from "./resendOtp.js"
import { authState, retrieveCachedAuthenticated, setAuthenticated } from "../authState.js"

const authApp = document.querySelector("#auth-app")

export const renderVerifyEmailPage = () => {
    const title = document.querySelector("#title")
    const body= document.querySelector("body")

    title.textContent = "Verify Email"
    body.dataset.page = "verify-email";

    const html = `
    <form id="verify-email-form" action="" method="PATCH">

        <label for="otp">OTP</label>
        <input id="otp" type="text" name="otp" >

        <button id="verify">Verify</button>
        <button id="resend" data-action="resend">Resend</button>
    </form>
    `
    authApp.innerHTML = "";
    authApp.innerHTML = html;

    verifyEmailEventListener()
  }



export const handleVerifyEmail = async (event) => {
    event.preventDefault();

    const button = event.target;
    console.log(button)

    if (button.id!== "resend" && button.id !== "verify"){
      return null;
    }

    console.log(button.id)

    if (button.id === "resend") {
          handleResendOtp(event)
          return null;
      }

    let user = null;

    if (authState.user) {
        user = authState.user
    }else {
        user = retrieveCachedAuthenticated().user;
    }

    if (!user) {
        navigateAuth("register")
    }

  const form = event.target.closest("form")
  const otpCode= form.otp.value

  try {
    const response = await verifyEmail(otpCode, user.public_id);
    if (!response.success) {
        console.log(response.message)
    }

    setAuthenticated(response.data.user, response.data.access_token);
    sessionStorage.setItem("user", JSON.stringify(response.data.user))
    window.location.assign("/app"); 

  } catch (error) {
    console.log(error)
  }
};


export const verifyEmailEventListener = async () => {
    const form = document.querySelector("#verify-email-form");
    form.addEventListener("click", handleVerifyEmail)
};
