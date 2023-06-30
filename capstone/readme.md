# Wiki v2 #
## Distinctiveness and Complexity ##
This project was based on Project 1, Wiki, with added functionality. Back when I was doing project 1, I noticed there were some key features missing, such as an approval system for editing and a way to communicate with each other. This results in edits being done without other people checking if the changes made were correct. It also meant there was no way for users to directly communicate with each other through the site. I also felt saving articles in separate files was problematic. This was because if admins want to delete an article, they need direct access to the server with the files to delete them. Finally, the project was lacking in security as anyone could create articles and edit them, making it easy to vandalise articles.  
As such, I believe this project is distinctive and complex as it does a major overhaul to how wiki was done. Users are required to be logged in to create articles, propose changes to articles and comment on both articles and edits. Articles are now also stored in the database for admins to be able to delete them, even without physical access to the server. Admins are given permission to approve edits to articles and revert to previous versions of an article is neccessary.  
I believe this project is distinctive from other submitted projects as an approval system based on Github’s pull request system was added, along with an algorithm to track changes (based on github’s own method of tracking changes) made in an edit and a failsafe system to revert previous changes should there be a need to (including up to the original version of the article). The system also incorporates javascript to minimise reloading the websites for any action done.  
Finally, the ability to comment was added for both articles and edits to allow logged in users to easily communicate their opinions of articles and edits.
## Steps to run the project ##
1. Run `pip -r requirements.txt` (for markdown module depenency)
2. Run `python manage.py runserver`
## Contents in the folder ##
* `wiki/templates/wiki/` contains all templates used in the app
    * `login.html` contains the login page.  
    * `register.html` contains the register page.  
    * `layout.html` contains the sidebar for the entire app (which becomes a header in mobile view for mobile responsiveness) and is where `styles.css` and `index.js` are attached to. It contains hyperlinks to login, register, view articles user has followed (when logged in), logout and a search bar to search for an article. If the search bar is able to find an exact article title with the user’s query, it sends the user there. Otherwise, it sends the user to `query.html`.  
    * `query.html` is used to display a list of results when a person makes searches for an article through the search bar in `layout.html` and a an exact result is not returned.  
    * `index.html` is the index page of the wiki and displays a list of all articles in bullet point. Clicking on an article sends the user to the article page.  
    * `following.html` displays a list of articles the user follows in a similar fashion to `index.html`
    * `create.html` is the page used for creating articles. On submission, the article contents are sent through a form to the backend and the user is sent back to the index page.  
    * `article.html` displays an article, along with its comments, a text box to comment and buttons to edit, view lists of edits of the article, follow and unfollow it. Each comment contains the comment along with the username of the commented and the timestamp of when the comment was made.
    * `edit.html` displays the form for editing an article.  
    * `edits.html` displays a list of edits the article has. Each edit comes with a display of what was removed and added at which sentence to summarise edits done, along with its approval status, the user that made the edit and the user that approved or rejected the edit. There is also a button for admins to revert the article back to the original version.  
    * `edit_view.html* displays the contents of the edit. For admins, there are also buttons to either approve or reject an edit if it is still pending approval. If the edit is approved and is not the latest version, a button to revert to this version of the article is shown for the admin. It also contains comments and a text box to comment.
* `wiki/static/wiki` contains `styles.css` and `index.js`
    * `styles.css` is used to touch up on web styling. Most of the styling is done via bootstrap classes in the templates. In particular, `styles.css` is responsible for the mobile responsiveness of the sidebar.
    * `index.js` contains various functions to minimise reloading of the page to visually update it and to send data to the back-end by using the FETCH API.
        * `following` is used to follow and unfollow an article by sending an empty FETCH request to `follow` in `views.py` when the follow/unfollow button is clicked. It also updates the button as appropriate after following/unfollowing.
        * `check_follow` is used to change the text content of the follow button to unfollow if the user has followed the article when entering the article page.
        * `comment` is used to send a user comment in an article to `edit_comment` in `views.py` via a FETCH request. It also displays the comment at the top of the comments list so that users need not reload the page to see their new comment.
        * `edit_comment` is used to send a user comment in an edit to `edit_comment` in `views.py` via a FETCH request . It also displays the comment at the top of the comments list so that users need not reload the page to see their new comment.
        * `approve` is used to either approve or reject an edit by sending `action` (either `accept` or `reject`) to `edit_view` in `views.py` and to remove the buttons for approving and rejecting after approval/rejection.
        * `revert` is used to revert an article to a previous version by sending an empty FETCH request to `revert` in `views.py`. It then sends the user back to the article view.
        * `revert_original` is used to revert and article to the original version by sending an empty FETCH request to `revert_original` in `views.py`. It then sends the user back to the article view.
* `wiki/models.py` contains six models
    * `Article` is used to store the contents of the article, the title of the article, when it was created, the user who created it and an edit timestamp.
    * `Original_Article` is used to archive the original version of the article should there be a need to revert to it.
    * `Comment` is used to store the comment, the user who made the comment, the timestamp of the comment and the article the comment belongs to.
    * `Edit` is used to store the contents of the edit, the title of the edit, the user who created the edit, the timestamp the edit was made, the status of the edit (0 means pending approval, 1 means approved and 2 means rejected) and the user who approved the edit, if accepted or rejected.
    * `Following` is used to store the article being followed and the user following the article.
    * `Edit_Comment` is used to store the contents of the comment, the user who made the comment, the timestamp of the comment and the edit the comment belongs to
* `wiki/util.py` contains the file necessary to track changes.
    * `track_changes` orchestrates the procedure to track changes.
    * `body_to_array` converts a body of paragraph into an array of sentence, where each sentence from a paragraph is in a list, and in turn each paragraph list is nested in a body list.
    * `check_changes` compares the differences between the old and new version of the article sentence by sentence. Currently, it does not highlight a sentence is changed if it is merely placed in a different location without the contents of the sentence being changed (though semantically this edge case should rarely occur).
* `wiki/views.py` contains the logic needed to run the website.
    * `login_view` handles logins of user accounts.
    * `logout_view` handles logouts of user accounts.
    * `register` handles registration of user accounts.
    * `index` displays all articles in a list in the index page.
    * `create` handles both rendering of the form for creating an article via a GET request and sending the newly created article data to both the `Article` model and the `Original_Article` model (for archival should there be a need to revert to the original version) via a POST request.
    * `article` handles rendering of an article and its comments.
    * `edits` handle the displaying of the list edits of an article, with the data of each edit being stored in a nested array. Data of the edit itself and the differences `track_changes` from `util.py` detects are stored in a list, which is nested within a list of all edits of an article.
    * `edit` handles both rendering of the form for editing an article via a GET request and sending the newly created edit data to the `Edit` model via a POST request.
    * `edit_view` handles the rendering of the edit, its comments and the button to revert to that version of the edit if the edit is approved and not the latest version via a GET request. The approval or rejection of an edit depending on the `action` sent through the FETCH request is also handled.
    * `following` handles the logic behind a user following and unfollowing an article via a FETCH request
    * `query` handles the search bar logic. If an article with the exact title the user queried is found, it redirects the user to that article page. Otherwise, it uses regex to generate a list of articles that starts with what the user queried.
    * `comment` acts as an endpoint to send newly created comments in articles via a FETCH request to the `Comment` model.
    * `edit_comment` acts as an endpoint to send newly created comments in edits via a FETCH request to the `Edit_Comment` model.
    * `revert` acts as an endpoint to receive revert requests via FETCH and to handle the logic in reverting articles to a previously approved version.
    * `revert_original` acts as an endpoint to receive FETCH requests and handle the logic to revert an article to its original version.
