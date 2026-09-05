import { getFollowingList, follow, unfollow } from "./api.js";
import { setFollowState, retrievecachedFollowState, updateFollowState } from "./followState.js";

export const handleGetFollowingsList = async () => {
    try {
        const response = await getFollowingList("posts");

        if (!response.success) {
            console.log(response.message);
        }

        console.log(response.data)
        setFollowState(response.data)

    } catch (error) {
        console.log(error.message)
    };
};


export const handleFollow = async (event) => {
    event.preventDefault()

    const button = event.target.closest("[data-button=follow-button]")
    const actions = new Set(["follow", "unfollow"])
    const buttonAction = button?.dataset?.action;

    if (!actions.has(buttonAction)) {
        return null;
    }
    console.log(button)
    console.log(buttonAction)
    const followedUserID = button.dataset.userId

    if (buttonAction === "follow") {
        button.setAttribute("class", "btn btn-primary-outline")
        button.textContent = "following"
        button.dataset.action = "unfollow"
        try {
            const response = await follow(followedUserID)
            console.log(response)
            if (!response.success) {
                button.setAttribute("class", "btn btn-primary")
                button.textContent = "follow"
                button.dataset.action = "follow"
            }
            updateFollowState(followedUserID) 
            console.log(button) 

        } catch (error) {
            console.log(error)
            button.setAttribute("class", "btn btn-primary")
            button.textContent = "follow"
            button.dataset.action = "follow"
            
        }
        return

    } 

    if (buttonAction === "unfollow") {
        button.setAttribute("class", "btn btn-primary")
        button.textContent = "follow"
        button.dataset.action = "follow"

        try {
            const response = await unfollow(followedUserID)
            if (!response.success) {
                button.setAttribute("class", "btn btn-primary-outline")
                button.textContent = "following"
                button.dataset.action = "unfollow"
            }
            updateFollowState(followedUserID, "unfollow")  
            
        } catch (error) {
            console.log(error)
            button.setAttribute("class", "btn btn-primary-outline")
            button.textContent = "following"
            button.dataset.action = "unfollow"
        } 
        return    
    }
}