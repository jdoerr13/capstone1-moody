



// Code from friends_groups.html

document.addEventListener('DOMContentLoaded', function () {
    // Your code here
    document.getElementById('toggleUsersButton').addEventListener('click', function () {
        console.log("Button clicked"); // Add this line for debugging
        const userSearchForm = document.getElementById('userSearchForm');
        const searchResults = document.getElementById('searchResults');

        if (userSearchForm.style.display === 'none') {
            userSearchForm.style.display = 'block';
            searchResults.style.display = 'block';
        } else {
            userSearchForm.style.display = 'none';
            searchResults.style.display = 'none';
        }
    });
    });


// Send friend request using AJAX
document.addEventListener('DOMContentLoaded', function () {
document.querySelectorAll('.send-friend-request').forEach(function (sendButton) {
    sendButton.addEventListener('click', function (event) {
        event.preventDefault();
        const userId = this.getAttribute('data-user-id');

        // Send a POST request to send a friend request
        fetch(`/send_friend_request/${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the UI or show a success message
                alert('Friend request sent successfully.');
            } else {
                // Handle errors or show an error message
                alert(data.message); // Display the error message from the JSON response
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the friend request.');
        });
    });
});
});


//Accept friend request:
$(document).ready(function () {
    // Handle "Accept" button click
    $('.accept-button').click(function () {
        // Store the reference to the clicked button
        var acceptButton = $(this);

        var userId = acceptButton.data('user-id');

        // Send an AJAX request to accept the friend request
        $.post(`/accept_friend_request/${userId}`, function (data) {
            if (data.success) {
                // Remove the accepted friend request from the received friend requests section
                acceptButton.parent().remove();

                // Move the accepted friend to the friends list
                var friendUsername = acceptButton.siblings('span').text();
                var newFriendItem = `<li>${friendUsername}</li>`;
                $('.friends-list ul').append(newFriendItem);
            } else {
                // Handle errors if needed
                console.log('Friend request acceptance failed.');
            }
        });
    });

    // Remove Friend: 
    $('.remove-friend-button').click(function () {
        var friendId = $(this).data('user-id');

        // Send an AJAX request to remove the friend
        $.post(`/remove_friend/${friendId}`, function (data) {
            if (data.success) {
                // Friend removed successfully
                alert('Friend removed successfully');
                // Optionally, you can reload the page or update the UI as needed
            } else {
                // Display error message using Flask flash or handle the error accordingly
                alert('An error occurred while removing the friend.');
            }
        });
    });
});

// Join group using AJAX
document.querySelectorAll('.join-group').forEach(function (joinLink) {
    joinLink.addEventListener('click', function (event) {
        event.preventDefault();
        const group_id = this.getAttribute('data-group-id');

        // Send a POST request to join the group
        fetch(`/join_group/${group_id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
            })
            .then(() => {
                // Redirect to the group page
                window.location.href = `/group/${group_id}`;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while joining the group.');
            });
    });
});




// Code from group.html

document.addEventListener('DOMContentLoaded', function () {
    // Function to add a post to the discussion forum
    function addPostToDiscussion(username, content, timestamp, post_id) {
        const post = document.createElement("div");
        post.className = "post";
        post.innerHTML = `<p>${username} says:</p><p>${content}</p><p>Posted on ${timestamp}</p>`;

        if (g.user && post_id === g.user.user_id) {
            const deleteForm = document.createElement("form");
            deleteForm.method = "post";
            deleteForm.action = `/delete_post/${post_id}`;

            const deleteButton = document.createElement("button");
            deleteButton.type = "submit";
            deleteButton.className = "delete-post-button";
            deleteButton.textContent = "Delete";

            deleteForm.appendChild(deleteButton);

            post.appendChild(deleteForm);
            post.innerHTML += '<p>My Post</p>';
        }

        document.getElementById("discussion").appendChild(post);
    }

    // Function to create a new post
    async function createNewPost(content) {
        try {
            const groupId = window.location.pathname.match(/\/group\/(\d+)/);
            if (groupId) {
                const response = await fetch(`/create_group_post/${groupId[1]}`, {
                    method: "POST",
                    body: new URLSearchParams({ post_content: content }),
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                });

                if (response.ok) {
                    const postData = await response.json();
                    addPostToDiscussion(postData.username, postData.content, postData.timestamp, postData.post_id);
                    document.getElementById("post-content").value = "";
                }
            } else {
                console.error("Group ID not found in the URL.");
            }
        } catch (error) {
            console.error("Error creating a new post:", error);
        }
    }

    // Check if local storage has posts and display them
    const storedPosts = JSON.parse(localStorage.getItem("discussionPosts")) || [];
    storedPosts.forEach((post) => {
        addPostToDiscussion(post.username, post.content, post.timestamp, post.userId);
    });

    document.getElementById("post-form").addEventListener("submit", async function (event) {
        event.preventDefault();
        const content = document.getElementById("post-content").value;
        if (content) {
            await createNewPost(content);
        }
    });
    
    // JavaScript code to fetch and display group members
    const seeGroupMembersButton = document.getElementById("seeGroupMembersButton");

    seeGroupMembersButton.addEventListener("click", async () => {
        fetchAndDisplayGroupMembers();
    });
});

// JavaScript code to fetch and display group members
document.addEventListener('DOMContentLoaded', function () {
const seeGroupMembersButton = document.getElementById("seeGroupMembersButton");

// Function to fetch and display group members
async function fetchAndDisplayGroupMembers() {
    const groupMembers = document.getElementById("groupMembers");
    const groupId = seeGroupMembersButton.getAttribute("data-group-id"); // Get the group_id from the button's data attribute

    // Make a request to the server to get group members
    try {
        const response = await fetch(`/get_group_members/${groupId}`, {
            method: 'GET',
        });

        if (response.ok) {
            const data = await response.json();

            if (data.length > 0) {
                groupMembers.innerHTML = '<h3>Group Members:</h3>';
                const ul = document.createElement("ul");

                data.forEach(member => {
                    const li = document.createElement("li");
                    li.textContent = member.username;
                    ul.appendChild(li);
                });

                groupMembers.appendChild(ul);
            } else {
                groupMembers.innerHTML = '<p>No group members found.</p>';
            }

            groupMembers.style.display = "block";
        } else {
            console.error('Failed to fetch group members:', response.statusText);
            groupMembers.innerHTML = '<p>Failed to fetch group members.</p>';
            groupMembers.style.display = "block";
        }
    } catch (error) {
        console.error('Error fetching group members:', error);
        groupMembers.innerHTML = '<p>Failed to fetch group members.</p>';
        groupMembers.style.display = "block";
    }
}

seeGroupMembersButton.addEventListener("click", () => {
    fetchAndDisplayGroupMembers();
});
});
