import { resetPassword, verifyEmail } from "../authApi.js"
import { authState, retrieveCachedAuthenticated, setAuthenticated } from "../authState.js"
import { navigateAuth } from "../authViews.js";

const authApp = document.querySelector("#auth-app")

const params = new URLSearchParams(window.location.search);
const token = params.get("token");
console.log(token)

export const renderResetPasswordPage = () => {

    if (!token) {
        console.log("No token detected")
        navigateAuth("login")
    }

    const title = document.querySelector("#title")
    const body= document.querySelector("body")

    title.textContent = "Reset Password"
    body.dataset.page = "reset-password";

    const html = `
    <form id="reset-password-form" action="" method="PATCH">

        <label for="password">New Password</label>
        <input id="password" type="password" name="password" placeholder="irir9494#">

        <label for="confirm-password">Confirm password</label>
        <input id="confirm-password" type="password" name="confirm_password" placeholder="irir9494#">

        <button id="reset" type="submit">Reset</button>
    </form>
    `
    authApp.innerHTML = "";
    authApp.innerHTML = html;

    resetPasswordEventListener()
  }


export const handleResetPassword= async (event) => {
    event.preventDefault();

    const form = event.target;
    const password = form.password.value;
    const confirm_password = form.confirm_password.value;


  try {
    const response = await resetPassword(token, password, confirm_password);
    if (!response.success) {
        console.log(response.message)
    }

    console.log(response.message)
    navigateAuth("login"); 

  } catch (error) {
    console.log(error)
  }
};


export const resetPasswordEventListener = async () => {
    const form = document.querySelector("#reset-password-form");
    form.addEventListener("submit", handleResetPassword)
};
