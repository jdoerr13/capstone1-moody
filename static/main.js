//current.html

    document.getElementById('show-json-btn').addEventListener('click', function () {
        document.querySelector('.json-container').style.display = 'block';
    });


//wellness.html

    document.addEventListener('DOMContentLoaded', function () {
        const goalsList = document.getElementById('goalsList');
        const newGoalInput = document.getElementById('newGoal');
        const addGoalButton = document.getElementById('addGoal');
        const deleteCompletedGoalsButton = document.getElementById('deleteCompletedGoals');

        addGoalButton.addEventListener('click', function () {
            const newGoalText = newGoalInput.value.trim();
            if (newGoalText) {
                addGoal(newGoalText);
                newGoalInput.value = '';
            }
        });

        deleteCompletedGoalsButton.addEventListener('click', function () {
            deleteCompletedGoals();
        });

        function addGoal(goalText) {
            const listItem = document.createElement('li');

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';

            const goalLabel = document.createElement('label');
            goalLabel.textContent = goalText;

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete';
            deleteButton.addEventListener('click', function () {
                deleteGoal(listItem);
            });

            listItem.appendChild(checkbox);
            listItem.appendChild(goalLabel);
            listItem.appendChild(deleteButton);

            goalsList.appendChild(listItem);
        }

        function deleteCompletedGoals() {
            const checkboxes = document.querySelectorAll('#goalsList input[type="checkbox"]');
            checkboxes.forEach(function (checkbox) {
                if (checkbox.checked) {
                    const listItem = checkbox.parentElement;
                    deleteGoal(listItem);
                }
            });
        }
        function deleteGoal(listItem) {
            goalsList.removeChild(listItem);
        }
    });



    const journalEntriesDiv = document.getElementById("journalEntries");
    const toggleJournalButton = document.getElementById("toggleJournalButton");
    let isJournalVisible = false;

    toggleJournalButton.addEventListener("click", function () {
        isJournalVisible = !isJournalVisible;
        if (isJournalVisible) {
            journalEntriesDiv.style.display = "block";
            toggleJournalButton.textContent = "Hide Entries";
        } else {
            journalEntriesDiv.style.display = "none";
            toggleJournalButton.textContent = "See Entries";
        }
    });



    document.addEventListener('DOMContentLoaded', function () {
        const journalForm = document.getElementById("journalForm");
        const journalEntryInput = document.getElementById("journalEntry");
        const journalEntriesDiv = document.getElementById("journalEntries");

        // Function to display journal entries
        function displayJournalEntries(entries) {
    journalEntriesDiv.innerHTML = "";  // Clear the existing entries

    if (entries.length > 0) {
        const ul = document.createElement("ul");

        entries.forEach(entry => {
            const li = document.createElement("li");

            // Create a span to display the entry text
            const entryTextSpan = document.createElement("span");
            entryTextSpan.textContent = `${entry.date} (#${entry.id})`;

            // Create an "Edit" button
            const editButton = document.createElement("button");
            editButton.textContent = "Edit";
            editButton.className = "btn btn-primary btn-sm";
            editButton.addEventListener("click", () => {
                window.location.href = `/edit_journal_entry/${entry.id}`;
                });

            // Append the entry text and "Edit" button to the list item
            li.appendChild(entryTextSpan);
            li.appendChild(editButton);

            ul.appendChild(li);
        });

        journalEntriesDiv.appendChild(ul);
    } else {
        journalEntriesDiv.innerHTML = '<p>No journal entries available.</p>';
    }
}

    // Function to fetch and display journal entries
    function fetchAndDisplayJournalEntries() {
        // Fetch journal entries from the server using a fetch request
        fetch('/fetch_journal_entries') //POTENTIALLY UPDATE TO AXIOS for CSRF protection
            .then((response) => response.json())
            .then((entries) => { //chaining
                // Display the fetched journal entries
                displayJournalEntries(entries);
            })
            .catch((error) => {
                console.error('Error fetching journal entries:', error);
            });
    }

        // Handle form submission
        journalForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            const journalEntry = journalEntryInput.value.trim();

            if (journalEntry) {
                try {
                    const response = await fetch('/save_journal_entry', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ entry: journalEntry }),
                    });

                    if (response.ok) {
                        // Entry saved successfully, so fetch and display journal entries again
                        fetchAndDisplayJournalEntries();
                        journalEntryInput.value = "";
                    } else {
                        console.error('Failed to save journal entry:', response.statusText);
                    }
                } catch (error) {
                    console.error('Error saving journal entry:', error);
                }
            }
        });

            // Fetch and display journal entries when the page loads
        fetchAndDisplayJournalEntries();
    });





    // Toggle mood history:
    document.addEventListener('DOMContentLoaded', function () {
        const moodHistory = document.getElementById('moodHistory');
        const toggleButton = document.getElementById('toggleMoodHistory');
        const averageMoodData = document.getElementById('averageMoodData');

        // Hide the mood history initially
        moodHistory.style.display = 'none';
        averageMoodData.style.display = 'none'; // Hide the average data

        // Toggle mood history when the button is clicked
        toggleButton.addEventListener('click', function () {
            if (moodHistory.style.display === 'none') {
                moodHistory.style.display = 'block';
                averageMoodData.style.display = 'block'; // Show the average data
                toggleButton.textContent = 'Hide Mood History';
            } else {
                moodHistory.style.display = 'none';
                averageMoodData.style.display = 'none'; // Hide the average data
                toggleButton.textContent = 'Show Mood History';
            }
        });
    });
    

    document.addEventListener('DOMContentLoaded', async function () {
        // Initialize the FullCalendar
        const calendarEl = document.getElementById('calendar');
        const calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridWeek', // Display a week view by default
            events: [], // No initial events
            // Set a fixed height for the calendar
            height: 275,
        });

        // Render the calendar
        calendar.render();

        // Get the user's location from the template
        const userLocation = '{{ user_location }}';



    async function updateWeatherData() {
        const options = {
            method: 'GET',
            url: 'https://weatherapi-com.p.rapidapi.com/forecast.json',
            params: {
                q: userLocation,
                days: '3',
                units: 'imperial', // imperial for Fahrenheit
            },
            headers: {
                'X-RapidAPI-Key': 'eb3fa9d2eamsh622acd4eaa00bf3p19fc73jsn647406a37c4e',
                'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com',
            },
        };

    try { //store the response
        const response = await axios.request(options);//pause execution of async function until this promise is fulfilled- extracts resolved value

        // Extract and format weather data for the next 3 days
        const weatherData = response.data.forecast.forecastday;

        // Loop through the next 3 days and add the weather to the calendar
        for (let i = 0; i < 3; i++) {
            const dayWeather = weatherData[i];
            const date = dayWeather.date;
            const temperatureF = dayWeather.day.avgtemp_f + '°F'; // Temperature in Fahrenheit
            calendar.addEvent({
                title: `${dayWeather.day.condition.text} (${temperatureF})`,
                start: date,
                rendering: 'background',
                allDay: true,
            });
        }

        // Fetch and display the latest assessment data for the current day
        const today = new Date();
        const formattedToday = today.toISOString().split('T')[0];
        fetchLatestAssessment(formattedToday);
    } catch (err) {
        console.error('Error fetching weather data:', err);
    }
}
        // Initialize weather data and assessment data
    await updateWeatherData();


        // Function to toggle between week and month views
        let isFullMonth = false;
        function toggleView() {
            isFullMonth = !isFullMonth;
            const newView = isFullMonth ? 'dayGridMonth' : 'dayGridWeek';
            calendar.changeView(newView);
            document.getElementById('toggleView').textContent = isFullMonth ? 'See Current Week' : 'See Full Month';
        }

        // Attach the toggleView function to the button's click event
        document.getElementById('toggleView').addEventListener('click', toggleView);
    });

//group.html

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




//diagnosis_history.html

    // show/hide the diagnosis information
    document.getElementById('show-diagnosis-button').addEventListener('click', function () {
        let diagnosisInfo = document.getElementById('diagnosis-info');
        if (diagnosisInfo.style.display === 'none' || diagnosisInfo.style.display === '') {
            diagnosisInfo.style.display = 'block';
        } else {
            diagnosisInfo.style.display = 'none';
        }
    });

//edit_journal.html

    document.addEventListener('DOMContentLoaded', function () {
        const deleteButton = document.getElementById('delete-entry');
        const deleteForm = document.getElementById('delete-form');
        const submitButton = document.getElementById('submit-entry');

        deleteButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            const confirmation = confirm("Are you sure you want to delete this entry?");
            if (confirmation) {
                // Submit the delete form
                deleteForm.submit();
            }
        });

        submitButton.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default form submission
            const confirmation = confirm("Are you sure you want to update this entry?");
            if (confirmation) {
                // Submit the update form directly
                document.getElementById('edit-form').submit();
            }
        });
    });

//home.html
 
    $(document).ready(function() {
        // Attach a click event handler to all "leave group" buttons
        $('.leave-group-button').click(function() {
            let groupId = $(this).data('group-id');

            // Make an AJAX request to the server to leave the group
            $.post('/leave_group/' + groupId, function(data) {
                if (data.success) {
                    // Remove the group element from the "my groups" list
                    $(`.group[data-group-id="${groupId}"]`).remove();
                }
            });
        });
    });

    // JavaScript to toggle "Works Cited" content
    const worksCitedButton = document.getElementById("worksCitedButton");
    const worksCitedContent = document.getElementById("worksCitedContent");

    worksCitedButton.addEventListener("click", () => {
        if (worksCitedContent.style.display === "none") {
            worksCitedContent.style.display = "block";
        } else {
            worksCitedContent.style.display = "none";
        }
    });


//friends_groups.html

    // Toggle the visibility of the search results
    document.getElementById('toggleUsersButton').addEventListener('click', function () {
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
            const acceptButton = $(this);

            const userId = acceptButton.data('user-id');

            // Send an AJAX request to accept the friend request
            $.post(`/accept_friend_request/${userId}`, function (data) {
                if (data.success) {
                    // Remove the accepted friend request from the received friend requests section
                    acceptButton.parent().remove();

                    // Move the accepted friend to the friends list
                    const friendUsername = acceptButton.siblings('span').text();
                    const newFriendItem = `<li>${friendUsername}</li>`;
                    $('.friends-list ul').append(newFriendItem);
                } else {
                    // Handle errors if needed
                    console.log('Friend request acceptance failed.');
                }
            });
        });

        // Remove Friend: 
        $('.remove-friend-button').click(function () {
            const friendId = $(this).data('user-id');

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