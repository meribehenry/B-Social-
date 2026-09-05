// import { react, deleteReaction, getReactionList } from "../reaction/api.js";
// import { postsState, setPostsState } from "./postsState.js";
// import { thumbsUpOutline, thumbsUpSolid, thumbsDownOutline, thumbsDownSolid } from "./postDom.js";


// export const handleGetPostReactionsList = async () => {
//     if (localStorage.getItem("cachedPostsState")) {
//         return null;
//     }
//     try {
//         const response = await getReactionList("posts");

//         if (!response.success) {
//             console.log(response.message);
//         }

//         setPostsState(response.data.liked, response.data.diskliked)

//     } catch (error) {
//         console.log(error.message)
//     };
// };

// export const handlePostLikeReaction = async (postElement) => {
//     let buttonState = null;
//     const post = postElement 
//     const likeIcon = postElement.querySelector(".like-icon");
//     const dislikeIcon = postElement.querySelector(".dislike-icon");
//     // const dislikeCount = postElement.querySelector(".dislike-count")
//     const likeCount = postElement.querySelector(".like-count");
//     const postId = postElement.dataset.postId;

//     // Checks if post is already liked
//     if (likeIcon.dataset.reaction === "liked"){
//         likeIcon.src = thumbsUpOutline; // Changes the svg to outline
//         likeIcon.dataset.reaction = "none"

//         const oldLikeCount = Number(likeCount.textContent) // Store old like count just in case of any error
//         likeCount.textContent = oldLikeCount - 1; // Decrease like count

//         try {
//             const response = await deleteReaction("posts", postId) // Send the delete request to the backend
//             if (!response.success) {
//                 // Undo previous action
//                 likeIcon.src = thumbsDownSolid // Change svg back to solid
//                 likeCount.textContent = oldLikeCount; // Increase like count back
//                 likeIcon.dataset.reaction = "liked"
//                 return
//             }

//             // If responses succeeds get the cached post state and remove the post id from the likedPostIds list
//             const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState")) 
//             cachedPostsState.likedPostIds = cachedPostsState.likedPostIds.filter(item => item !== postId)
//             localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState)); // Save changes back to localStorage

//         } catch {
//             // Catch unknown error and undo previous action 
//             likeIcon.src = "../../../svgs/reaction/thumbs-up-solid.svg" // Change svg back to solid
//             likeCount.textContent = oldLikeCount; // Increase like count back
//             likeIcon.dataset.reaction = "liked"
//         }
//     } else {
//         // This runs when post has not been liked

//         const reactionType = "like";
//         let wasDisliked = false;
//         // const oldDislikeCount = dislikeCount.textContent // Store old dislike count just in case of any error

//         if (dislikeIcon.dataset.reaction === "disliked") {
//             dislikeIcon.src = "../../../svgs/reaction/thumbs-down-outline.svg"
//             dislikeIcon.dataset.reaction = "none"
//             // dislikeCount = oldDislikeCount  // Decrease the dislike count if post was previous disliked
//             wasDisliked = true;
//         }

//         likeIcon.src = "../../../svgs/reaction/thumbs-up-solid.svg"; // Change like button to a solid svg
//         likeIcon.dataset.reaction = "liked"

//         const oldLikeCount = Number(likeCount.textContent) // Store old like count just in case of any error
//         likeCount.textContent = oldLikeCount + 1;

//         try {
//             const response = await react("posts", postId, reactionType) // Send the request to the backend
//             if (!response.success) {
//                 // Undo previous action

//                 if (wasDisliked) {
//                     dislikeIcon.src = "../../../svgs/reaction/thumbs-down-solid.svg" // Change back to solid svg
//                     dislikeIcon.dataset.reaction = "disliked"
//                     // dislikeCount = oldDislikeCount // Increase dislike count back
//                 }

//                 likeIcon.src = "../../../svgs/reaction/thumbs-up-outline.svg";
//                 likeIcon.dataset.reaction = "none"
//                 likeCount.textContent = oldLikeCount; // Decrease the like count
//                 return
//             };

//             const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState")) 

//             // Delete the postId from the dislikedPostIds list if it was previously disliked
//             if (wasDisliked) {
//                 cachedPostsState.dislikedPostIds = cachedPostsState.dislikedPostIds.filter(item => item !== postId); 
//             };

//             cachedPostsState.likedPostIds.push(postId)
//             localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState)); // Save changes back to localStorage
//             return

//         } catch {
//             // Catch unknown error and undo previous action 
//             if (wasDisliked) {
//                 dislikeIcon.src = "../../../svgs/reaction/thumbs-down-solid.svg" // Change back to solid svg
//                 dislikeIcon.dataset.reaction = "disliked"
//                 // dislikeCount = oldDislikeCount // Increase dislike count back
//                 }

//                 likeIcon.src = "../../../svgs/reaction/thumbs-up-outline.svg";
//                 likeCount.textContent = oldLikeCount; // Decrease the like count
//                 likeIcon.dataset.reaction = "none"
//             }    
//     }
// };


// export const handlePostDislikeReaction = async (postElement) => {
//     console.log("Here")
//     let buttonState = null;
//     const post = postElement 
//     const likeIcon = post.querySelector(".like-icon");
//     const dislikeIcon = post.querySelector(".dislike-icon");
//     // const dislikeCount = post.querySelector(".dislike-count")
//     const likeCount = post.querySelector(".like-count");
//     const postId = post.dataset.postId;

//     // Checks if the dislike button already has the filled svg
//     if (dislikeIcon.dataset.reaction === "disliked"){
//         dislikeIcon.src = "../../../svgs/reaction/thumbs-down-outline.svg"; // Changes the svg to outline
//         dislikeIcon.dataset.reaction = "none"


//         // const oldDislikeCount = dislikeCount.textContent // Store old dislike count just in case of any error
//         // dislikeCount.textContent = oldDislikeCount - 1; // Decrease dislike count

//         try {
//             const response = await deleteReaction("posts", postId) // Send the delete request to the backend
//             if (!response.success) {
//                 // Undo previous action
//                 dislikeIcon.src = "../../../svgs/reaction/thumbs-down-solid.svg" // Change svg back to solid
//                 dislikeIcon.dataset.reaction = "disliked"
//                 // dislikeCount.textContent = oldDislikeCount; // Increase like count back
//                 return
//             }

//             // If responses succeeds get the cached post state and remove the post id from the likedPostIds list
//             const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState")) 
//             cachedPostsState.diskliked = cachedPostsState.dislikedPostIds.filter(item => item !== postId)
//             localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState)); // Save changes back to localStorage
//             return

//         } catch {
//             // Catch unknown error and undo previous action 
//             dislikeIcon.src = "../../../svgs/reaction/thumbs-down-solid.svg" // Change svg back to solid
//             dislikeIcon.dataset.reaction = "disliked"
//             // dislikeCount.textContent = oldDislikeCount; // Increase like count back
//             }

//     } else {
//         // This runs when post has not been disliked

//         const reactionType = "dislike";
//         let wasLiked = false;
//         const oldlikeCount = Number(likeCount.textContent) // Store old like count just in case of any error

//         if (likeIcon.dataset.reaction === "liked") {
//             likeIcon.src = "../../../svgs/reaction/thumbs-up-outline.svg";
//             likeIcon.dataset.reaction = "none"
//             likeCount.textContent = oldlikeCount - 1
//             wasLiked = true;;
//         };

//         dislikeIcon.src = "../../../svgs/reaction/thumbs-down-solid.svg";
//         dislikeIcon.dataset.reaction = "disliked"

//         // const oldDislikeCount = dislikeCount.textContent; // Store old dislike count just in case of any error
//         // dislikeCount.textContent = oldDislikeCount + 1;

//         try {
//             const response = await react("posts", postId, reactionType) // Send the request to the backend
//             if (!response.success) {
//                 // Undo previous action
//                 if (wasLiked) {
//                     likeIcon.src = "../../../svgs/reaction/thumbs-up-solid.svg" // Change back to solid svg
//                     likeIcon.dataset.reaction = "liked"
//                     likeCount.textContent = oldlikeCount // Increase like count back
//                 }

//                 dislikeIcon.src = "../../../svgs/reaction/thumbs-down-outline.svg";
//                 dislikeIcon.dataset.reaction = "none"
//                 // dislikeCount.textContent = oldDislikeCount; // Decrease the like count
//                 return
//             }

//             // If response succeeds update the state in local storage
//             const cachedPostsState = JSON.parse(localStorage.getItem("cachedPostsState")) 

//             // Delete the postId from the likedPostIds list if it was previously liked
//             if (wasLiked) {
//                 cachedPostsState.likedPostIds = cachedPostsState.likedPostIds.filter(item => item !== postId); 
//             };

//             cachedPostsState.dislikedPostIds.push(postId)
//             localStorage.setItem("cachedPostsState", JSON.stringify(cachedPostsState)); // Save changes back to localStorage
//             return

//         } catch {
//             // Catch unknown error and undo previous action 
//                 if (wasLiked) {
//                     likeIcon.src = "../../../svgs/reaction/thumbs-up-solid.svg" // Change back to solid svg
//                     likeIcon.dataset.reaction = "liked"
//                     likeCount.textContent = oldlikeCount // Increase like count back
//                 }

//                 dislikeIcon.src = "../../../svgs/reaction/thumbs-down-outline.svg";
//                 dislikeIcon.dataset.reaction = "none"
//                 // dislikeCount.textContent = oldDislikeCount; // Decrease the like count
//             };    
//         };
// };

import { react, deleteReaction, getReactionList } from "../reaction/api.js";
import { postsState, setPostsState, updatePostsState, retrieveCachedPostsState } from "./postsState.js";
import { thumbsUpOutline, thumbsUpSolid, thumbsDownOutline, thumbsDownSolid } from "./postDom.js";


export const handleGetPostReactionsList = async () => {
    if (localStorage.getItem("cachedPostsState")) {
        retrieveCachedPostsState()
        return null;
    }
    try {
        const response = await getReactionList("posts");

        if (!response.success) {
            console.log(response.message);
        }

        setPostsState(response.data.liked, response.data.disliked)

    } catch (error) {
        console.log(error.message)
    };
};

export const handlePostLikeReaction = async (postElement) => {
    let buttonState = null;
    const post = postElement 
    const likeIcon = postElement.querySelector(".like-icon");
    const dislikeIcon = postElement.querySelector(".dislike-icon");
    // const dislikeCount = postElement.querySelector(".dislike-count")
    const likeCount = postElement.querySelector(".like-count");
    const postId = postElement.dataset.postId;

    // Checks if post is already liked
    if (likeIcon.dataset.reaction === "liked"){
        likeIcon.src = thumbsUpOutline; // Changes the svg to outline
        likeIcon.dataset.reaction = "none"

        const oldLikeCount = Number(likeCount.textContent) // Store old like count just in case of any error
        likeCount.textContent = oldLikeCount - 1; // Decrease like count

        try {
            const response = await deleteReaction("posts", postId) // Send the delete request to the backend
            if (!response.success) {
                // Undo previous action
                likeIcon.src = thumbsUpSolid // Change svg back to solid
                likeCount.textContent = oldLikeCount; // Increase like count back
                likeIcon.dataset.reaction = "liked"
                return
            }

            updatePostsState({likedPostId:postId, isDelete:true})

        } catch (error) {
            // Catch unknown error and undo previous action 
            likeIcon.src = thumbsUpSolid // Change svg back to solid
            likeCount.textContent = oldLikeCount; // Increase like count back
            likeIcon.dataset.reaction = "liked"
            console.log(error)
            
        }
    } else {
        // This runs when post has not been liked

        const reactionType = "like";
        let wasDisliked = false;
        // const oldDislikeCount = dislikeCount.textContent // Store old dislike count just in case of any error

        if (dislikeIcon.dataset.reaction === "disliked") {
            dislikeIcon.src = thumbsDownOutline
            dislikeIcon.dataset.reaction = "none"
            // dislikeCount = oldDislikeCount  // Decrease the dislike count if post was previous disliked
            wasDisliked = true;
        }

        likeIcon.src = thumbsUpSolid; // Change like button to a solid svg
        likeIcon.dataset.reaction = "liked"

        const oldLikeCount = Number(likeCount.textContent) // Store old like count just in case of any error
        likeCount.textContent = oldLikeCount + 1;

        try {
            const response = await react("posts", postId, reactionType) // Send the request to the backend
            if (!response.success) {
                // Undo previous action

                if (wasDisliked) {
                    dislikeIcon.src = thumbsDownSolid // Change back to solid svg
                    dislikeIcon.dataset.reaction = "disliked"
                    // dislikeCount = oldDislikeCount // Increase dislike count back
                }

                likeIcon.src = thumbsUpOutline;
                likeIcon.dataset.reaction = "none"
                likeCount.textContent = oldLikeCount; // Decrease the like count
                return
            };

            updatePostsState({likedPostId:postId})
            return

        } catch (error) {
            // Catch unknown error and undo previous action 
            if (wasDisliked) {
                dislikeIcon.src = thumbsDownSolid // Change back to solid svg
                dislikeIcon.dataset.reaction = "disliked"
                // dislikeCount = oldDislikeCount // Increase dislike count back
                }

                likeIcon.src = thumbsUpOutline;
                likeCount.textContent = oldLikeCount; // Decrease the like count
                likeIcon.dataset.reaction = "none"
                console.log(error) 
            }  
             
    }
};


export const handlePostDislikeReaction = async (postElement) => {
    let buttonState = null;
    const post = postElement 
    const likeIcon = post.querySelector(".like-icon");
    const dislikeIcon = post.querySelector(".dislike-icon");
    // const dislikeCount = post.querySelector(".dislike-count")
    const likeCount = post.querySelector(".like-count");
    const postId = post.dataset.postId;

    // Checks if the dislike button already has the filled svg
    if (dislikeIcon.dataset.reaction === "disliked"){
        dislikeIcon.src = thumbsUpOutline; // Changes the svg to outline
        dislikeIcon.dataset.reaction = "none"


        // const oldDislikeCount = dislikeCount.textContent // Store old dislike count just in case of any error
        // dislikeCount.textContent = oldDislikeCount - 1; // Decrease dislike count

        try {
            const response = await deleteReaction("posts", postId) // Send the delete request to the backend
            if (!response.success) {
                // Undo previous action
                dislikeIcon.src = thumbsDownSolid // Change svg back to solid
                dislikeIcon.dataset.reaction = "disliked"
                // dislikeCount.textContent = oldDislikeCount; // Increase like count back
                return
            }

            updatePostsState({dislikedPostId:postId, isDelete:true})
            return

        } catch (error){
            // Catch unknown error and undo previous action 
            dislikeIcon.src = thumbsDownSolid // Change svg back to solid
            dislikeIcon.dataset.reaction = "disliked"
            // dislikeCount.textContent = oldDislikeCount; // Increase like count back
            console.log(error)
            }

    } else {
        // This runs when post has not been disliked

        const reactionType = "dislike";
        let wasLiked = false;
        const oldlikeCount = Number(likeCount.textContent) // Store old like count just in case of any error

        if (likeIcon.dataset.reaction === "liked") {
            likeIcon.src = thumbsUpOutline;
            likeIcon.dataset.reaction = "none"
            likeCount.textContent = oldlikeCount - 1
            wasLiked = true;;
        };

        dislikeIcon.src = thumbsDownSolid;
        dislikeIcon.dataset.reaction = "disliked"

        // const oldDislikeCount = dislikeCount.textContent; // Store old dislike count just in case of any error
        // dislikeCount.textContent = oldDislikeCount + 1;

        try {
            const response = await react("posts", postId, reactionType) // Send the request to the backend
            if (!response.success) {
                // Undo previous action
                if (wasLiked) {
                    likeIcon.src = thumbsUpSolid // Change back to solid svg
                    likeIcon.dataset.reaction = "liked"
                    likeCount.textContent = oldlikeCount // Increase like count back
                }

                dislikeIcon.src = thumbsDownOutline;
                dislikeIcon.dataset.reaction = "none"
                // dislikeCount.textContent = oldDislikeCount; // Decrease the like count
                return
            }

            updatePostsState({dislikedPostId:postId})
            return

        } catch (error) {
            // Catch unknown error and undo previous action 
                if (wasLiked) {
                    likeIcon.src = thumbsUpSolid // Change back to solid svg
                    likeIcon.dataset.reaction = "liked"
                    likeCount.textContent = oldlikeCount // Increase like count back
                }

                dislikeIcon.src = thumbsUpOutline;
                dislikeIcon.dataset.reaction = "none"
                // dislikeCount.textContent = oldDislikeCount; // Decrease the like count
                console.log(error)
            };   

        };
};
