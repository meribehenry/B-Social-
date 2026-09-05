import { resendOtp } from "../authApi.js";
import { authState, retrieveCachedAuthenticated} from "../authState.js";
import { navigateAuth } from "../authViews.js";

export const handleResendOtp = async (event) => {
    event.preventDefault();

    let user = null;

    if (authState.user) {
        user = authState.user
    }else {
        user = retrieveCachedAuthenticated().user;
    }

    if (!user) {
        navigateAuth("register")
    }


    try {
    const response = await resendOtp(user.public_id);
    if (!response.success) {
        console.log(response.message)
    }

    console.log("OTP resent")

    } catch (error) {
    console.log(error)
    }
};