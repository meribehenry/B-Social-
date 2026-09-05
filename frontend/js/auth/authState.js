export let authState = {
    user: null,
    accessToken: null,
    isAuthenticated: false,
    // initialised: false
};


export const setUser = (user) =>  {
    authState.user =  user || {};

    const cachedAuthenticated = {
        user: user,
        isAuthenticated: false
    } 

    sessionStorage.setItem("cachedAuthenticated", JSON.stringify(cachedAuthenticated))
};

export const setToken = (accessToken) =>  {
    authState.accessToken =  accessToken;
    authState.isAuthenticated = true

    const cachedAuthenticated = JSON.parse(localStorage.getItem("cachedAuthenticated"))
    cachedAuthenticated.isAuthenticated = true
    localStorage.setItem("cachedAuthenticated", JSON.stringify(cachedAuthenticated))   

    
};

export const clearToken = () =>  {
    authState.accessToken =  null;
    authState.isAuthenticated = false

    const cachedAuthenticated = JSON.parse(localStorage.getItem("cachedAuthenticated"))
    cachedAuthenticated.isAuthenticated = false
    localStorage.setItem("cachedAuthenticated", JSON.stringify(cachedAuthenticated))   
};


export const setAuthenticated = (user, accessToken, cache=true) =>  {
    authState.user =  user || {};
    authState.accessToken =  accessToken;
    authState.isAuthenticated = true

    if (cache) {
        const cachedAuthenticated = {
            user: user,
            isAuthenticated: true
        } 

        localStorage.setItem("cachedAuthenticated", JSON.stringify(cachedAuthenticated))
    }
};



export const retrieveCachedAuthenticated = () => {
    const cachedAuthenticated = JSON.parse(localStorage.getItem("cachedAuthenticated"))
    authState.user = cachedAuthenticated?.user
    authState.isAuthenticated = cachedAuthenticated?.isAuthenticated
    return authState
}

export const clearAuth = () =>  {
    authState.user =  null;
    authState.accessToken =  null;
    authState.isAuthenticated = false;

    localStorage.removeItem("cachedAuthenticated")
};