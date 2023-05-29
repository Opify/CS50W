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
  load_mailbox('inbox');
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
    <div class="form-group">Subject: ${mail.subject}</div>
    <div class="form-group"><textarea class="form-control" disabled placeholder="Body">${mail.body}</textarea></div>
    <div class="form-group">Timestamp: ${mail.timestamp}</div>`
    // archive email logic
    if (mail.archived) {
      const archive = document.createElement('button');
      archive.textContent = "Un-archive";
      archive.id = "archive";
      document.querySelector('#email-view').append(archive);
    } else {
      const archive = document.createElement('button');
      archive.textContent = "Archive";
      archive.id = "archive";
      document.querySelector('#email-view').append(archive);
    }
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !mail.archived
        })
      });
      load_mailbox('inbox');
    });
    const reply = document.createElement('button');
    reply.textContent = "Reply";
    reply.id = "reply";
    reply.addEventListener('click', () => reply_email(mail.sender, mail.subject, mail.body, mail.timestamp));
    document.querySelector('#email-view').append(reply);
  })
  .then(fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  }))
}

// Task 5 (done)
function reply_email(sender, subject, body, timestamp) {
  compose_email();
  document.querySelector('#compose-recipients').value = sender;
  // use regex to check if Re is in subject field
  const regex = /^Re: /;
  if (regex.test(subject)) {
    document.querySelector('#compose-subject').value = subject
  } else {
    document.querySelector('#compose-subject').value = `Re: ${subject}`
  }
  document.querySelector('#compose-body').value = `\nOn ${timestamp} ${sender} wrote:\n${body}`
}