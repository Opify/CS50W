document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.post-div').forEach((div) => get_likes(div))
    document.querySelectorAll('.post-div').forEach((div) => check_like(div))
    document.querySelectorAll('.edit').forEach((post) => post.addEventListener('click', (event) => edit(event)))
    document.querySelectorAll('.like').forEach((post) => post.addEventListener('click', (event) => like(event)))
})

// Task 6 (done)
function edit(event) {
    const div = event.target.parentElement
    const edit = div.querySelector('.content')
    const content = edit.innerHTML
    const editing = document.createElement('textarea')
    editing.class = "editing"
    editing.value = content
    const confirmation = document.createElement('button')
    confirmation.textContent = "Confirm Edit"
    confirmation.className = "confirmation"
    edit.replaceWith(editing)
    event.target.replaceWith(confirmation)
    confirmation.addEventListener('click', () => {
        modify(div.id, editing.value, editing, div)
    })
}

function modify(id, contents, current, div) {
    fetch(`/edit/${id}`, {
        method: "PUT",
        headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
        body: JSON.stringify({
            content: contents
        }),
        mode: 'same-origin'
    })
    const updated = document.createElement('p')
    updated.className = "content"
    updated.textContent = contents
    current.replaceWith(updated)
    const done = document.createElement('button')
    done.className = "edit"
    done.textContent = "Edit"
    div.querySelector('.confirmation').replaceWith(done)
    done.addEventListener('click', (event) => edit(event))
}

// Task 7 (done)
function get_likes(div) {
    id = div.id
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then((json) => {
        div.querySelector('.likes').textContent = `${json["likes"]}`
    })
}

function check_like(div) {
    id = div.id
    fetch(`/check_like/${id}`)
    .then(response => response.json())
    .then((json) => {
        if (json["liked"] === "true") {
            const target = div.querySelector('.like')
            const unlike = document.createElement('button')
            unlike.className = "like"
            unlike.textContent = "Unlike"
            unlike.addEventListener('click', like)
            target.replaceWith(unlike)
        }
    })
}

function like(event) {
    const div = event.target.parentElement
    const id = div.id
    if (event.target.textContent === "Like") {
        fetch(`/like/${id}`, {
            method: "POST",
            headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
            mode: 'same-origin'
        })    
        const unlike = document.createElement('button')
        unlike.className = "like"
        unlike.textContent = "Unlike"
        unlike.addEventListener('click', like)
        event.target.replaceWith(unlike)
        div.querySelector('.likes').textContent = parseInt(div.querySelector('.likes').textContent) + 1
    } else if (event.target.textContent === "Unlike") {
        fetch(`/like/${id}`, {
            method: "POST",
            headers: {'X-CSRFToken': document.cookie.replace('csrftoken=', '')},
            mode: 'same-origin'
        })    
        const relike = document.createElement('button')
        relike.className = "like"
        relike.textContent = "Like"
        relike.addEventListener('click', like)
        event.target.replaceWith(relike)
        div.querySelector('.likes').textContent = parseInt(div.querySelector('.likes').textContent) - 1
    }
}