

async function newComment(event) {
    comment.removeEventListener("click",newComment)
    console.log("clicked")
    comment.innerHTML = `
    <textarea id="edit-text" name="comment-text" maxlength="250" required>${curComment}</textarea>
    <input type="submit" id="edit-submit-button" value="Submit Edit">
    `
}
let comment = document.getElementById("comment-abc")
let curComment = comment.innerText
comment.addEventListener("click", newComment)