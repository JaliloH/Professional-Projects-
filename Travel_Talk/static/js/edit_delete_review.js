// I made this to prevent merge conflicts, 
// we can place it into another file after

// set listeners for deleting posts n stuff
document.addEventListener("DOMContentLoaded", function() {
    let submitEditButtons = document.querySelectorAll(".submit-edit");
    submitEditButtons.forEach((submitEditButton) => {
        submitEditButton.classList.remove("show");
        submitEditButton.classList.add("hide");
        submitEditButton.addEventListener("click", submitEditHandler);
    })

    let deleteButtons = document.querySelectorAll(".delete");
    deleteButtons.forEach((deleteButton) => {
        deleteButton.addEventListener("click", deleteHandler);
    })

    let editButtons = document.querySelectorAll(".edit");
    editButtons.forEach((editButton) => {
        editButton.addEventListener("click", editHandler);
    })
    // Add like count later?


});

async function editHandler(e) {
    // let postId = e.target.getAttribute("data-post-id");
    // const postBlock = document.getElementById(`post_${postId}`)
    const submitEditButton = postBlock.querySelector(".submit-edit");
    submitEditButton.classList.add("show");
    submitEditButton.classList.remove("hide");

    const textElement = postBlock.querySelector(".review-text")
    textElement.style.backgroundColor= "#bcddad"
    textElement.contentEditable = true;
}


