// async function newPic(event) {
//     avatar.removeEventListener("click", newPic)
    
//     uploadPfp = document.getElementById("profile-pfp-update")
//     uploadPfp.innerHTML += `
//     <div>
//         <label for="avatar">Select image:</label>
//         <input type="file" id="avatar" name="avatar" accept="image/png"> 
//         <button class="profile-button" type="submit" style="margin-top: 6px">Update Avatar</button>
//     `
//     // or we can do accept="image/*"
// }

async function newUsername(event) {
    username.removeEventListener("click", newUsername)
    
    username.innerHTML = `
    <textarea class="pure-form" id="username" name="username" placeholder="${curUsername}" minlength="1" maxlength="50" row="2" cols="38" required></textarea>
    <button class="profile-button" type="submit">Update Username</button>
    `
}

// let avatar = document.getElementById("profile-pfp")
// avatar.addEventListener("click", newPic)

let username = document.getElementById("profile-username")
let curUsername = username.innerText
username.addEventListener("click", newUsername)