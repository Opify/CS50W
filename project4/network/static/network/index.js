document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit').forEach((post) => post.addEventListener('click', (event) => edit(event)))
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