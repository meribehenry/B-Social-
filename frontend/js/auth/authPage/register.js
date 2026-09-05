import { register } from "../authApi.js";
import { setUser } from "../authState.js";
import { navigateAuth } from "../authViews.js";

const authApp = document.querySelector("#auth-app")

export const renderRegisterPage = () => {
    const title = document.querySelector("#title")
    const body= document.querySelector("body")

    title.textContent = "Register"
    body.dataset.page = "register";

    const html = `
    <form id="register-form" action="" method="POST">

        <label for="firstname">Firstname</label>
        <input id="firstname" type="text" name="firstname" placeholder="Johnny">

        <label for="lastname">Lastname</label>
        <input id="lastname" type="text" name="lastname" placeholder="Dep">

        <label for="email">Email</label>
        <input id="email" type="email" name="email" placeholder="john@example.com">

        <label for="password">Password</label>
        <input id="password" type="password" name="password" placeholder="irir9494#">

        <label for="confirm-password">Confirm password</label>
        <input id="confirm-password" type="password" name="confirm_password" placeholder="irir9494#">

        <input type="radio" name="gender" value="male">Male
        <input type="radio" name="gender" value="female">Female 

        <button type="submit">Register</button>
    </form>
    `
    authApp.innerHTML = "";
    authApp.innerHTML = html;

    registerEventListener()

};


export const handleRegister = async (event) => {
  event.preventDefault();

  const form = event.target;
  const firstname = form.firstname.value.trim();
  const lastname = form.lastname.value.trim();
  const email = form.email.value.trim();
  const password = form.password.value;
  const confirm_password = form.confirm_password.value;
  const gender = form.gender.value;

  try {
    const response = await register(email, password, confirm_password, firstname, lastname, gender);
    if (!response.success) {
        console.log(response.message)
    }

    setUser(response.data)
    navigateAuth("verify-email");

  } catch (error) {
    console.log(error.message)
  }
};




export const registerEventListener = async () => {
    const form = document.querySelector("#register-form");
    form.addEventListener("submit", handleRegister)
};