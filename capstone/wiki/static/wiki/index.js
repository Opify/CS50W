document.addEventListener('DOMContentLoaded', function() {
    try {
        document.querySelector('.follow').addEventListener('click', (event) => follow(event))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        check_follow(document.querySelector('.follow'))
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
        document.querySelectorAll('.approve').forEach((elem) => elem.addEventListener('click', (event) => approve(event)))
    }
    catch {
        // Why cant we have a pass 
    }
})

function follow(event) {
    event.preventDefault()
    const id = event.target.id
    fetch(`/follow/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        mode: 'same-origin'
    })    
    if (event.target.value === "Follow") {
        event.target.value = "Unfollow"
    } else if (event.target.value === "Unfollow") {
        event.target.value = "Follow"
    }
}

function check_follow(follow) {
    id = follow.id
    fetch(`/follow/${id}`)
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
        div.innerHTML = `<p>${user}</p>
        <p>${timestamp}</p>
        <p>${comment}</p>`
        const root = document.querySelector('#comment-view')
        root.prepend(div)
        })
}

function approve(event) {
    const id = event.target.parentElement.id
    const action = event.target.id
    fetch(`/view_edit/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        body: JSON.stringify({
            action: action
        }),
        mode: 'same-origin'
    })
    event.target.parentElement.style.display = 'none'
}