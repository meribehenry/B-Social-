import {renderLoginPage} from "./authPage/login.js"
import { renderRegisterPage } from "./authPage/register.js";
import { renderVerifyEmailPage } from "./authPage/verifyEmail.js";
import { register } from "./authApi.js";
import { renderResetRequestPage } from "./authPage/resetRequest.js";
import { renderResetPasswordPage } from "./authPage/resetPassword.js";


export const renderAuthView = (view) => {
    switch ( view) {
        case "login":
            renderLoginPage();
            break;
        
        case "register":
            renderRegisterPage();
            break;

        case "verify-email":
            renderVerifyEmailPage();
            break;

        case "reset-request":
            renderResetRequestPage();
            break;

        case "reset-password":
            renderResetPasswordPage();
            break;

        default: 
            renderLoginPage();
    }
}

export const navigateAuth = (view) => {
    const url = `/auth?view=${encodeURIComponent(view)}`
    history.pushState(
    {}
    , 
    "", 
    url
    )

    renderAuthView(view)
}


