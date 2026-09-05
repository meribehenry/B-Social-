import { handleGetFollowingsList } from "./followAction.js"

export const followState = {
    followedUserIds: new Set()
}

export const setFollowState = (follwedUserIds, cache=true) => {
    followState.followedUserIds = new Set(follwedUserIds)

    if (cache) {
        const cachedFollowState = {
        followedUserIds: follwedUserIds
        }

        localStorage.setItem("cachedFollowState", JSON.stringify(cachedFollowState))
    }
}

export const updateFollowState = (followedUserId, action="follow") => {
    const actions = new Set(["follow", "unfollow"])

    if (!actions.has(action)) {
        console.log("Invaild action type")
        return null;
    }

    const cachedFollowState = JSON.parse(localStorage.getItem("cachedFollowState"))

    if (action === "follow") {
        followState.followedUserIds.add(followedUserId)
        cachedFollowState.followedUserIds.push(followedUserId)
    }

    if (action === "unfollow") {
        followState.followedUserIds.delete(followedUserId)
        cachedFollowState.followedUserIds = cachedFollowState.followedUserIds.filter(item => item !== followedUserId);
    }

    localStorage.setItem("cachedFollowState", JSON.stringify(cachedFollowState))
}

export const retrievecachedFollowState = () => {
    const cachedFollowState = JSON.parse(localStorage.getItem("cachedFollowState"))

    if (cachedFollowState.followedUserIds){
        setFollowState(cachedFollowState.followedUserIds, false)
        return
    }
    handleGetFollowingsList()
}

export const clearFollowState = ()  => {
    followState.followedUserIds = null;

    localStorage.removeItem("cachedFollowState")

}

export const setDOMFollowState = (author, followButton) => {
    if (Object.keys(followState).length ===0) {
        retrievecachedFollowState()
    }
    console.log("What is it")
    if (followState.followedUserIds.has(author.public_id)){
            followButton.textContent = "following";
            followButton.setAttribute("class", "btn btn-primary-outline")
            followButton.dataset.action = "unfollow"
    } else {
        followButton.textContent = "follow";
        followButton.setAttribute("class", "btn btn-primary")
        followButton.dataset.action = "follow"
    }

}