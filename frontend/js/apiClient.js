import { authState, clearAuth, clearToken, setAuthenticated, setToken } from "./auth/authState.js";


const API_BASE_URL = "/api/v1";

let accessToken = null;
let refreshPromise = null;


// ==================================================
// MAIN API REQUEST
// ==================================================

export const apiRequest = async (
    path,
    requestOptions = {},
    config = {},
    ) => {

    const {
        retryOn401 = true
    } = config;


    const url = `${API_BASE_URL}${path}`;
    // const url = path;


    // ----------------------------------------------
    // HEADERS
    // ----------------------------------------------

    const headers = {
            // "Content-Type": "application/json",
            ...requestOptions.headers
        };
        
    // ----------------------------------------------
    // BEARER TOKEN
    // ----------------------------------------------

    if (authState.accessToken) {
        headers["Authorization"] =
            `Bearer ${authState.accessToken}`;
        }

    // ----------------------------------------------
    // SEND REQUEST
    // ----------------------------------------------

    const response = await fetch(url, {

        ...requestOptions,

        headers,

        credentials: "include"

    });


    // ----------------------------------------------
    // ACCESS TOKEN EXPIRED
    // ----------------------------------------------

    if (
        response.status === 401 &&
        retryOn401
    ) {
        clearToken()

        const refreshed = await refreshAccessToken();


        if (refreshed) {

            return apiRequest(
                path,
                requestOptions,
                {
                    retryOn401: false
                }
            );

        };

        // Refresh failed.
        // The session is no longer valid.

        clearAuth();

        redirectToLogin();

        throw new Error(
            "Your session has expired."
        );
    }


    // ----------------------------------------------
    // PARSE RESPONSE
    // ----------------------------------------------

    const data =
        await parseResponse(response);


    // ----------------------------------------------
    // OTHER ERRORS
    // ----------------------------------------------

    if (!response.ok) {

        const error = new Error(
            data?.message ||
            "The request failed."
        );

        error.status = response.status;

        error.data = data;

        throw error;
    }


    return data;
}


// ==================================================
// REFRESH ACCESS TOKEN
// ==================================================

const refreshAccessToken = async () => {

  if (refreshPromise){
    return refreshPromise
  };

  refreshPromise = actuallyRefreshAccessToken();

  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }

};
  
  
const actuallyRefreshAccessToken = async () => {

    const response = await fetch(
        `${API_BASE_URL}/auth/refresh`,
        {
            method: "POST",
            headers: {
            "Content-Type": "application/json"
                },
            credentials: "include"
        }
    );


    if (!response.ok) {
        return false;
    };


    const data = await parseResponse(response);


    if (!data?.data?.access_token) {
        return false;
    };

    console.log(data)
    setToken(data.data.access_token)
    return true;
};


// ==================================================
// RESPONSE PARSER
// ==================================================

const parseResponse = async (response) => {

    const contentType =
        response.headers.get("content-type");


    if (
        contentType &&
        contentType.includes("application/json")
    ) {

        return await response.json();
    }

    return null;
}


// ==================================================
// REDIRECT
// ==================================================

const redirectToLogin = () => {

    window.location.href = "./auth";
};