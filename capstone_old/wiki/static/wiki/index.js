document.addEventListener('DOMContentLoaded', function() {
    try {
        document.querySelector('.follow').addEventListener('click', (event) => follow_article(event))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        check_follow_article(document.querySelector('.follow'))
    }
    catch {
        // Why cant we have a pass 
    }
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
        document.querySelector('.edit-comment-button').addEventListener('click', (event) => edit_comment(event))
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
    try {
        document.querySelector('#revert').addEventListener('click', (event) => revert(event))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        document.querySelector('.revert_original').addEventListener('click', (event) => revert_original(event))
    }
    catch {
        // Why cant we have a pass 
    }
    try {
        document.querySelectorAll('.article_approve').forEach((elem) => elem.addEventListener('click', (event) => article_approve(event)))
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

function follow_article(event) {
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

function check_follow_article(follow) {
    id = follow.id
    fetch(`/follow/${id}`)
    .then(response => response.json())
    .then((json) => {
        if (json["followed"] === "true") {
            follow.value = "Unfollow"
        }
    })
}

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

function edit_comment(event) {
    const edit_comment = event.target.parentElement.querySelector('#comment').value
    const id = event.target.id
    fetch(`/edit_comment/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        body: JSON.stringify({
            edit_comment: edit_comment
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
        <p>${edit_comment}</p>`
        const root = document.querySelector('#edit-comment-view')
        root.prepend(div)
        event.target.parentElement.querySelector('#comment').value = ""
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
    .then(() => {
        if (action === "accept") {
            window.location.replace(`/wiki/${event.target.dataset.article}`)
        } else {
            window.location.replace(`/view_edit/${id}`)
        }
    })
}

function article_approve(event) {
    const id = event.target.parentElement.id
    const action = event.target.id
    fetch(`/pending/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        body: JSON.stringify({
            action: action
        }),
        mode: 'same-origin'
    })
    .then(() => {
        if (action === "accept") {
            window.location.replace(`/wiki/${id}`)
        }
        else {
            window.location.replace(`/pending/${id}`)
        }
    })
}

function revert(event) {
    const id = event.target.parentElement.id
    const title = event.target.dataset.article
    fetch(`/revert/${id}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        mode: 'same-origin'
    })
    .then(() => {
        window.location.replace(`/wiki/${title}`)
    }) 
}

function revert_original(event) {
    const title = event.target.id
    fetch(`/revert_original/${title}`, {
        method: "POST",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        mode: 'same-origin'
    })
    .then(() => {
        window.location.replace(`/wiki/${title}`)
    }) 
}
