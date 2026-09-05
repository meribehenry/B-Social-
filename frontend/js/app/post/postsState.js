import { handleGetPostReactionsList } from "./postReaction.js";

export const postsState = {
    likedPostIds: new Set(),
    dislikedPostIds: new Set(),
    // postsCount: 0,
    // dislikedCount: 0

    };

export const setPostsState = (likedPostIds, dislikedPostIds, cache=true) => {
    postsState.likedPostIds = new Set(likedPostIds);
    postsState.dislikedPostIds = new Set(dislikedPostIds);

    if (cache) {
        const cachedPostsState = {
        likedPostIds: likedPostIds,
        dislikedPostIds: dislikedPostIds 
        }

        localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState))
        console.log(postsState)
    }
}

export const updatePostsState = ({likedPostId=null, dislikedPostId=null, isDelete=false}) => {
    const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState"))

    if (!isDelete) {
        if (likedPostId) {
            if (postsState.dislikedPostIds.has(likedPostId) || cachedPostsState.dislikedPostIds.includes(likedPostId)) {
                postsState.dislikedPostIds.delete(likedPostId); 
                cachedPostsState.dislikedPostIds = cachedPostsState.dislikedPostIds.filter(item => item !== likedPostId);
            }
            console.log(postsState)
            postsState.likedPostIds.add(likedPostId)
            cachedPostsState.likedPostIds.push(likedPostId)
        }
        if (dislikedPostId) {
            if (postsState.likedPostIds.has(dislikedPostId) || cachedPostsState.likedPostIds.includes(dislikedPostId)) {
                postsState.likedPostIds.delete(dislikedPostId); 
                cachedPostsState.likedPostIds = cachedPostsState.likedPostIds.filter(item => item !== dislikedPostId); 
            }

            postsState.dislikedPostIds.add(dislikedPostId)
            cachedPostsState.dislikedPostIds.push(dislikedPostId)
            const r = []
            r.includes()
        }
    } else {
        if (likedPostId) {
            if (postsState.likedPostIds.has(likedPostId) || cachedPostsState.likedPostIds.includes(likedPostId)) {
                console.log(postsState)
                postsState.likedPostIds.delete(likedPostId); 
                cachedPostsState.likedPostIds = cachedPostsState.likedPostIds.filter(item => item !== likedPostId);
                console.log(postsState)
            }
        }
        if (dislikedPostId) {
            if (postsState.dislikedPostIds.has(dislikedPostId) || cachedPostsState.dislikedPostIds.includes(dislikedPostId)) {
                postsState.dislikedPostIds.delete(dislikedPostId); 
                cachedPostsState.dislikedPostIds = cachedPostsState.dislikedPostIds.filter(item => item !== dislikedPostId); 
            }
        }
    }

    localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState))
}

export const retrieveCachedPostsState = () => {
    const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState"))
    if (cachedPostsState){
        setPostsState(cachedPostsState.likedPostIds, cachedPostsState.dislikedPostIds, false)
        return
    }
    handleGetPostReactionsList()
}

export const clearPostsState = ()  => {
    postsState.likedPostIds = null;
    postsState.dislikedPostIds = null;

    localStorage.removeItem("cachedPostsState")

} 