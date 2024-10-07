async function display() {
    const response = await fetch("/api/session")
    json = await response.json()

    if (json['exists']) {
        account = document.getElementById("menu-account")

        account.innerHTML = `
        <div class="dropdown">
        <button class="dropbtn">Welcome, ${json['user']['username']}</button>
            <div class="dropdown-content">
                <a href="/profile">Profile</a>
                <a href="/logout">Log Out</a>
            </div>
        </div>`
    }
    else {
        return
    }
}

document.addEventListener('DOMContentLoaded', display)