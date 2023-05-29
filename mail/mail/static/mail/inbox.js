document.addEventListener('DOMContentLoaded', function() {
  // create email-view div
  const target = document.createElement('div');
  target.id='email-view';
  document.querySelector('body').append(target);

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');

  document.querySelector('#compose-view').addEventListener('submit', send_mail);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

// Task 2 (done)
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get mail
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const element = document.createElement('div');
      if (email.read) {
        element.style.backgroundColor = "LightGray";
      } else {
        element.style.backgroundColor = "white";
      }
      element.className = "border border-dark email";
      element.innerHTML = `Sender: ${email.sender}<br>Subject: ${email.subject}<br>Timestamp: ${email.timestamp}`;
      element.addEventListener('click', () => read_mail(email.id));
      document.querySelector('#emails-view').append(element);
    });
  });
}

// Task 1 (done)
function send_mail(event) {
  event.preventDefault();
 fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json());
  return load_mailbox('inbox');
}

// Task 3, 4 (done)
function read_mail(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(mail => {
    // directly write html contents
    document.querySelector('#email-view').innerHTML = 
    `<div class="form-group">From: <input disabled class="form-control" value="${mail.sender}"></div>
    <div class="form-group">To: <input class="form-control" disabled value=${mail.recipients.toString()}></div>
    <div class="form-group">Subject: <input class="form-control" disabled placeholder="Subject" value=${mail.subject}></div>
    <div class="form-group"><textarea class="form-control" disabled placeholder="Body">${mail.body}</textarea></div>
    <div class="form-group">Timestamp: ${mail.timestamp}</div>`
    // archive email logic
    if (mail.archived) {
      const element = document.createElement('button')
      element.textContent = "Un-archive"
      element.id = "archive"
      document.querySelector('#email-view').append(element)
    } else {
      const element = document.createElement('button')
      element.textContent = "Archive"
      element.id = "archive"
      document.querySelector('#email-view').append(element)
    }
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !mail.archived
        })
      })
      return load_mailbox('inbox')
    })
  })
  .then(fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  }))
}