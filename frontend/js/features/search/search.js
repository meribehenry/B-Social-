import { getUserSearchResult } from "../../api/search.api.js";
import { renderPosts } from "../../components/post.js";
import { renderSearchResult } from "../../components/search.js";

const resultsSection = document.querySelector("#search-results-section")

export const handleGetUserSearchResult = async (event) => {
    event.preventDefault()
    const form = event.target
    const word = form.search.value.trim()

    try {
        const response = await getUserSearchResult(word);
        if (!response.success) {
        throw new Error(response.message);
        };

        const fragment = document.createDocumentFragment()

        for (const result of response.data.users) {
            if (result.posts) {
                const posts = renderPosts(result.posts)
                fragment.append(posts)
            } else {
                const user = renderSearchResult(result)
                fragment.append(user)
            }
        }
     
        resultsSection.innerHTML = ""
        resultsSection.append(fragment)

    } catch (error) {
        throw (error);
    }
};
