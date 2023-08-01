# Blog #
For my capstone project, I chose to create a blogsite, with the ability to comment, edit, customise the style of your posts and much more
## Distinctiveness and Complexity ##
I believe this project is distinct as it has never been done as a project in CS50W. Moreover, the website allows users to customise the fonts and background of their posts and profile page through CSS properties (including the possibility of using images as their background). Finally, unique to the project, groups were added to help categorise posts, allowing users to quickly see all posts related to the group. Users can also claim themselves to be interested in the group subject, allowing other users to notice them easier and follow them. In addition, small functionalities such as a post of the day and random posts were also added for further distinctiveness.

I believe this project is also complex as an algorithm was made from scratch to summarise changes (based on Github’s own method of tracking changes) made in an edit. The system also incorporates JavaScript to minimise reloading the websites for any action done. Finally, a custom pagination algorithm was used to easily browse posts made by the same user of the current post.
## Steps to run the project ##
1. Run `pip -r requirements.txt` (for markdown module dependency)
2. Run `python manage.py runserver`
## Contents in the folder ##
* `blog/templates/blog/` contains all templates used in the app
    * `login.html` contains the login page.  
    * `register.html` contains the register page.  
    * `layout.html` contains the sidebar for the entire app (which becomes a header in mobile view for mobile responsiveness) and is where `styles.css` and `index.js` are attached to. It contains hyperlinks to login, register, see all groups, see a random post, and a search bar to search for a post. If the search bar is able to find an exact post title with the user’s query, it sends the user there. Otherwise, it sends the user to `query.html`. For logged in users, it also contains hyperlinks to logout, create an post, and view all profiles the user is following. 
    * `query.html` is used to display a list of results when a person makes searches for an post through the search bar in `layout.html` and a an exact result is not returned.  
    * `index.html` is used to display the post of the day in a similar fashion to `post.html`.
    * `all_pages.html` is the index page of the blog and displays a list of all posts in bullet point. Clicking on a post sends the user to the post page.  
    * `following.html` displays a list of users the user follows in a similar fashion to `all_pages.html`.
    * `create.html` is the page used for creating posts and optionally linking them to multiple groups (Group1, Group2, …). On submission, the post contents are sent through a form to the backend and the user is sent back to the index page.  
    * `profile.html` is used to display a user's profile page which includes their bio and what they are an expert in. The user can also edit their own profile page or follow other users.
    * `edit_profile.html` is used to display the form to edit the user's profile page (including the background and their font colour to be used in their posts and profile page).
    * `post.html` displays an post, along with its comments, a text box to comment and buttons to edit, view lists of edits of the post, follow and unfollow it. Each comment contains the comment along with the username of the commented and the timestamp of when the comment was made.
    * `edit.html` displays the form for editing an post.  
    * `edits.html` displays a list of edits the post has. Each edit comes with a display of what was removed and added at which sentence to summarise edits done.
    * `edit_view.html` is used to display the contents of an edit
    * `groups.html` is used to display a list of all groups.
    * `group.html` is used to display a two separate lists of all experts and posts in the group.
* `blog/static/blog` contains `styles.css` and `index.js`
    * `styles.css` is used to touch up on web styling. Most of the styling is done via bootstrap classes in the templates. In particular, `styles.css` is responsible for the mobile responsiveness of the sidebar.
    * `index.js` contains various functions to minimise reloading of the page to visually update it and to send data to the back-end by using the FETCH API.
        * `follow_user` is used to follow and unfollow a user by sending an empty FETCH request to `profile` in `views.py` when the follow/unfollow button is clicked. It also updates the button as appropriate after following/unfollowing.
        * `check_follow_user` is used to change the text content of the follow button to unfollow if the user has followed the user when entering the post page by sending a blank FETCH request to `check_follow_user`.
        * `comment` is used to send a user comment in an post to `comment` in `views.py` via a FETCH request. It also displays the comment at the top of the comments list so that users need not reload the page to see their new comment.
* `blog/models.py` contains six models
    * `User` is used to create a bio field for users to include biographies of themselves in their profile page, their background preference and their font colour for their profile page and posts.
    * `Post` is used to store the contents of the post, the title of the post, when it was created, the user who created it, and an edit timestamp.
    * `Comment` is used to store the comment, the user who made the comment, the timestamp of the comment and the post the comment belongs to.
    * `Edit` is used to store the contents of the edit, the title of the edit, the user who created the edit, and the timestamp the edit was made.
    * `Following ` is used to store the user being followed and the user following them.
    * `Group` is used to store the group the post and user is in. It is optional for both posts and users.
* `blog/util.py` contains the file necessary to track changes.
    * `track_changes` orchestrates the procedure to track changes.
    * `body_to_array` converts a body of paragraph into an array of sentence, where each sentence from a paragraph is in a list, and in turn each paragraph list is nested in a body list.
    * `check_changes` compares the differences between the old and new version of the post sentence by sentence. Currently, it does not highlight a sentence is changed if it is merely placed in a different location without the contents of the sentence being changed (though semantically this edge case should rarely occur).
* `blog/views.py` contains the logic needed to run the website.
    * `login_view` handles logins of user accounts.
    * `logout_view` handles logouts of user accounts.
    * `register` handles registration of user accounts.
    * `all_pages` displays all posts in a list in the index page.
    * `index` displays an post of the day (currently just a random post).
    * `profile` displays the profile of a user. It also acts as and endpoint for FETCH requests to follow/unfollow a user by updating the `Following` model.
    * `edit_profile` is used to display the form for editing a user profile and to handle changes in a user's profile once the form is submitted through a POST request by updating the data in the `User` and `Following` models.
    * `check_follow_user` checks if the user is followed through `Following_Users` to update the text value of the follow button in `profile.html` by sending an appropriate json response.
    * `create` handles both rendering of the form for creating an post via a GET request and sending the newly created post data to the `Post` model, and the `Group` model (if a group was added) via a POST request.
    * `post` handles rendering of an post and its comments.
    * `random_post` displays a random post.
    * `edits` handle the displaying of the list edits of an post, with the data of each edit being stored in a nested array. Data of the edit itself and the differences `track_changes` from `util.py` detects are stored in a list, which is nested within a list of all edits of an post.
    * `edit` handles both rendering of the form for editing a post via a GET request and sending the newly created edit data to the `Edit` model via a POST request.
    * `edit_view` handles the rendering of the edit.
    * `following` is used to render the list of all profiles the user followed.
    * `query` handles the search bar logic. If an post with the exact title the user queried is found, it redirects the user to that post page. Otherwise, it uses regex to generate a list of posts that starts with what the user queried.
    * `comment` acts as an endpoint to send newly created comments in posts via a FETCH request to the `Comment` model.
    * `group_index` is used to display the list of all groups by getting a set of all groups from `Group`.
    * `group` is used to generate the two separate lists of posts and interested users in the group from `Group`.
