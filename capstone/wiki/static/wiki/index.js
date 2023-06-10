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
