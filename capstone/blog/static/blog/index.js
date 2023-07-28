document.addEventListener('DOMContentLoaded', function() {
    try {
        check_follow_user(document.querySelector('.follow_user'))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        document.querySelector('.comment-button').addEventListener('click', (event) => comment(event))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        document.querySelector('.follow_user').addEventListener('click', (event) => follow_user(event))
    }
    catch {
        // Why cant we have a pass 
    }
})

function follow_user(event) {
    const id = event.target.id
    fetch(`/profile/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        mode: 'same-origin'        
    })
    .then(() => {
        if (event.target.textContent == "Follow") {
            event.target.textContent = "Unfollow"
        } else if (event.target.textContent == "Unfollow") {
            event.target.textContent = "Follow"
        }
    })
}

function check_follow_user(follow) {
    id = follow.id
    fetch(`/follow_user/${id}`)
    .then(response => response.json())
    .then((json) => {
        if (json["followed"] === "true") {
            follow.value = "Unfollow"
        }
    })
}

function comment(event) {
    const comment = event.target.parentElement.querySelector('#comment').value
    const id = event.target.id
    fetch(`/comment/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        body: JSON.stringify({
            comment: comment
        }),
        mode: 'same-origin'
    })
    .then((response) => response.json())
    .then((json) => {
        try {
            document.querySelector('#no-comment').remove()
        }
        catch {
            // Why cant we have a pass 
        }
        const div = document.createElement('div')
        div.className = "border border-black"
        const user = json["user"]
        const timestamp = json["timestamp"]
        div.innerHTML = `<p><a href="/profile/${user}"/>${user}</a></p>
        <p>${timestamp}</p>
        <p>${comment}</p>`
        const root = document.querySelector('#comment-view')
        root.prepend(div)
        event.target.parentElement.querySelector('#comment').value = ""
        })
}