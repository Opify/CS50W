# Wiki v2 #
## Distinctiveness and Complexity ##
This project was based on Project 1, Wiki, with added functionality. Back when I was doing project 1, I noticed there were some key features missing, such as an approval system for editing and a way to communicate with each other. This results in edits being done without other people checking if the changes made were correct. It also meant there was no way for users to directly communicate with each other through the site. I also felt saving articles in separate files was problematic. This was because if admins want to delete an article, they need direct access to the server with the files to delete them. Finally, it can be difficult to easily see groups of articles together.  

As such, I believe this project is distinctive from other projects for five reasons. Firstly, articles are stored in a MySQL database instead of separate markdown files. This allows admins to delete articles instead of only the person who has physical access to the computer hosting the files. Secondly, articles and edits can now be commented on to allow communication on their opinions of articles and edits. Thirdly, unlike Project 1 where articles could be freely created and edited, all articles must receive admin’s approval for creating and editing them. This way, vandalism is almost improbable and ensures articles maintain a standard of quality. In addition, distinct from Project 1, users now have a profile page where they can describe more about themselves and show what they are an expert in. The articles they created are also displayed in their profile page, and users can follow them to see what new articles they have created. Comments also lead to the commentor’s profile page when clicked on. Finally, unique to the project, groups were added to help categorise articles, allowing users to quickly see all articles related to the group. Users can also claim themselves to be subject experts in the group, allowing other users to recognise them easier and follow them. In addition, small functionalities such as an article of the day and random articles were also added for further distinctiveness.

I believe this project is also complex as an approval system based on Github’s pull request system was added, along with an algorithm that was made from scratch to track changes (based on github’s own method of tracking changes) made in an edit and a failsafe system to revert previous changes should there be a need to (including up to the original version of the article). The system also incorporates javascript to minimise reloading the websites for any action done.  
## Steps to run the project ##
1. Run `pip -r requirements.txt` (for markdown module depenency)
2. Run `python manage.py runserver`
## Contents in the folder ##
* `wiki/templates/wiki/` contains all templates used in the app
    * `login.html` contains the login page.  
    * `register.html` contains the register page.  
    * `layout.html` contains the sidebar for the entire app (which becomes a header in mobile view for mobile responsiveness) and is where `styles.css` and `index.js` are attached to. It contains hyperlinks to login, register, see all groups and approved articles, see a random article, and a search bar to search for an article. If the search bar is able to find an exact article title with the user’s query, it sends the user there. Otherwise, it sends the user to `query.html`. For logged in users, it also contains hyperlinks to logout, create an article, check approval status of either articles created by the user (for non-admins) or approval status of all articles (for admins) and the users and articles the user is following. 
    * `query.html` is used to display a list of results when a person makes searches for an article through the search bar in `layout.html` and a an exact result is not returned.  
    * `index.html` is used to display the article of the day in a similar fashion to `article.html`.
    * `all_pages.html` is the index page of the wiki and displays a list of all articles in bullet point. Clicking on an article sends the user to the article page.  
    * `following.html` displays a list of articles and users the user follows in a similar fashion to `index.html`.
    * `create.html` is the page used for creating articles. On submission, the article contents are sent through a form to the backend and the user is sent back to the index page.  
    * `profile.html` is used to display a user's profile page which includes their bio and what they are an expert in. The user can also edit their own profile page or follow other users.
    * `edit_profile.html` is used to display the form to edit the user's profile page.
    * `approval_index.html` is used to display either a list of articles created by the user (for non-admins) or a list of articled created by all users (for admins). It includes the article title, the user who created the article and its approval status.
    * `approval_view.html` is used to display the contents of the article pending approval, along with its approval status. For admins, it also displays buttons to either accept or reject an article.
    * `article.html` displays an article, along with its comments, a text box to comment and buttons to edit, view lists of edits of the article, follow and unfollow it. Each comment contains the comment along with the username of the commented and the timestamp of when the comment was made.
    * `edit.html` displays the form for editing an article.  
    * `edits.html` displays a list of edits the article has. Each edit comes with a display of what was removed and added at which sentence to summarise edits done, along with its approval status, the user that made the edit and the user that approved or rejected the edit. There is also a button for admins to revert the article back to the original version.  
    * `edit_view.html` displays the contents of the edit. For admins, there are also buttons to either approve or reject an edit if it is still pending approval. If the edit is approved and is not the latest version, a button to revert to this version of the article is shown for the admin. It also contains comments and a text box to comment.
    * `groups.html` is used to display a list of all groups.
    * `group.html` is used to display a two separate lists of all experts and articles in the group.
* `wiki/static/wiki` contains `styles.css` and `index.js`
    * `styles.css` is used to touch up on web styling. Most of the styling is done via bootstrap classes in the templates. In particular, `styles.css` is responsible for the mobile responsiveness of the sidebar.
    * `index.js` contains various functions to minimise reloading of the page to visually update it and to send data to the back-end by using the FETCH API.
        * `follow_article_` is used to follow and unfollow an article by sending an empty FETCH request to `follow` in `views.py` when the follow/unfollow button is clicked. It also updates the button as appropriate after following/unfollowing.
        * `follow_user` is used to follow and unfollow a user by sending an empty FETCH request to `profile` in `views.py` when the follow/unfollow button is clicked. It also updates the button as appropriate after following/unfollowing.
        * `check_follow_article` is used to change the text content of the follow button to unfollow if the user has followed the article when entering the article page.
        * `comment` is used to send a user comment in an article to `edit_comment` in `views.py` via a FETCH request. It also displays the comment at the top of the comments list so that users need not reload the page to see their new comment.
        * `edit_comment` is used to send a user comment in an edit to `edit_comment` in `views.py` via a FETCH request . It also displays the comment at the top of the comments list so that users need not reload the page to see their new comment.
        * `approve` is used to either approve or reject an edit by sending `action` (either `accept` or `reject`) to `edit_view` in `views.py` and to remove the buttons for approving and rejecting after approval/rejection.
        * `article_approve` is used to either approve or reject a new article by sending `action` (either `accept` or reject) to `approve_view` in `views.py` and to remove the buttons for approving and rejecting after approval/rejection.
        * `revert` is used to revert an article to a previous version by sending an empty FETCH request to `revert` in `views.py`. It then sends the user back to the article view.
        * `revert_original` is used to revert and article to the original version by sending an empty FETCH request to `revert_original` in `views.py`. It then sends the user back to the article view.
* `wiki/models.py` contains six models
    * `User` is used to create a bio field for users to include biographies of themselves in their profile page.
    * `Article` is used to store the contents of the article, the title of the article, when it was created, the user who created it, the approval status of the article and an edit timestamp.
    * `Original_Article` is used to archive the original version of the article should there be a need to revert to it.
    * `Comment` is used to store the comment, the user who made the comment, the timestamp of the comment and the article the comment belongs to.
    * `Edit` is used to store the contents of the edit, the title of the edit, the user who created the edit, the timestamp the edit was made, the status of the edit (0 means pending approval, 1 means approved and 2 means rejected) and the user who approved the edit, if accepted or rejected.
    * `Following_Article` is used to store the article being followed and the user following the article.
    * `Following_User` is used to store the user being followed and the user following them.
    * `Edit_Comment` is used to store the contents of the comment, the user who made the comment, the timestamp of the comment and the edit the comment belongs to
    * `Group` is used to store the group the article and user is in (as an expert). It is optional for both articles and users.
* `wiki/util.py` contains the file necessary to track changes.
    * `track_changes` orchestrates the procedure to track changes.
    * `body_to_array` converts a body of paragraph into an array of sentence, where each sentence from a paragraph is in a list, and in turn each paragraph list is nested in a body list.
    * `check_changes` compares the differences between the old and new version of the article sentence by sentence. Currently, it does not highlight a sentence is changed if it is merely placed in a different location without the contents of the sentence being changed (though semantically this edge case should rarely occur).
* `wiki/views.py` contains the logic needed to run the website.
    * `login_view` handles logins of user accounts.
    * `logout_view` handles logouts of user accounts.
    * `register` handles registration of user accounts.
    * `all_pages` displays all articles in a list in the index page.
    * `index` displays an article of the day (currently just a random article).
    * `profile` displays the profile of a user. It also acts as and endpoint for FETCH requests to follow/unfollow a user by updating the `Following_User` model.
    * `edit_profile` is used to display the form for editing a user profile and to handle changes in a user's profile once the form is submitted through a POST request by updating the data in the `User` and `Following_User` models.
    * `create` handles both rendering of the form for creating an article via a GET request and sending the newly created article data to the `Article` model, the `Original_Article` model (for archival should there be a need to revert to the original version) and the `Group` model (if a group was added) via a POST request.
    * `approve_index` displays either all articles created by the user for non-admins, or all articles created by all users for admins. It displays the user who created the article and its approval status.
    * `approve_view` displays the article pending approval and its approval status. It also handles the approval/rejection of an article when the FETCH request is received.
    * `article` handles rendering of an article and its comments.
    * `random_article` displays a random article.
    * `edits` handle the displaying of the list edits of an article, with the data of each edit being stored in a nested array. Data of the edit itself and the differences `track_changes` from `util.py` detects are stored in a list, which is nested within a list of all edits of an article.
    * `edit` handles both rendering of the form for editing an article via a GET request and sending the newly created edit data to the `Edit` model via a POST request.
    * `edit_view` handles the rendering of the edit, its comments and the button to revert to that version of the edit if the edit is approved and not the latest version via a GET request. The approval or rejection of an edit depending on the `action` sent through the FETCH request is also handled by updating `Article` and `Group` models based on what is in the `Edit` model.
    * `follow_article` handles the logic behind a user following and unfollowing an article via a FETCH request
    * `following` is used to render the list of all users and articles the user followed.
    * `query` handles the search bar logic. If an article with the exact title the user queried is found, it redirects the user to that article page. Otherwise, it uses regex to generate a list of articles that starts with what the user queried.
    * `comment` acts as an endpoint to send newly created comments in articles via a FETCH request to the `Comment` model.
    * `edit_comment` acts as an endpoint to send newly created comments in edits via a FETCH request to the `Edit_Comment` model.
    * `revert` acts as an endpoint to receive revert requests via FETCH and to handle the logic in reverting articles to a previously approved version.
    * `revert_original` acts as an endpoint to receive FETCH requests and handle the logic to revert an article to its original version.
    * `group_index` is used to display the list of all groups by getting a set of all groups from `Group`.
    * `group` is used to generate the two separate lists of articles and experts in the group from `Group`.
