// Wait until the DOM (Document Object Model) is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Select all elements with the class 'reply-btn' and iterate over them
    document.querySelectorAll('.reply-btn').forEach(function (button) {
        // Add a click event listener to each 'reply-btn'
        button.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent the default action of the link
            // Get the value of the 'data-parent' attribute from the 
            // clicked button
            var parentId = this.getAttribute('data-parent');
            // Find the closest comment container and the nested comment 
            // form within it
            var parentComment = this.closest('.comments');
            var nestedForm = parentComment.querySelector(
                '.nested-comment-form');
            // Set the parent ID in the nested form's hidden input field
            nestedForm.querySelector('.parent-id').value = parentId;
            // Toggle the visibility of the nested comment form
            if (nestedForm.style.display === 'block') {
                // Hide the form if it's currently visible
                nestedForm.style.display = 'none';  
            } else {
                // Show the form if it's currently hidden
                nestedForm.style.display = 'block';  
            }
        });
    });

    // New code for handling like (upvote) button clicks
    document.querySelectorAll('.btn-like').forEach(function (button) {
        // Add a click event listener to each 'btn-like'
        button.addEventListener('click', function () {
            // Get the comment ID from the data-comment-id attribute
            var commentId = this.getAttribute('data-comment-id');
            // Get the CSRF (Cross-Site Request Forgery) token from the hidden 
            // input field in the comment form
            var csrfToken = document.querySelector(
                '[name=csrfmiddlewaretoken]').value;
            // Send an AJAX POST request to the upvote URL for the 
            // specified comment ID
            fetch(`/comment/upvote/${commentId}/`, {
                // Specify that the request method is POST
                method: 'POST',
                // Set the request headers
                headers: {
                    // Indicate that the request body contains JSON
                    'Content-Type': 'application/json',
                    // Include the CSRF token in the headers for security
                    'X-CSRFToken': csrfToken,
                },
            })
            // Handle the response from the fetch request and parse it as JSON
            .then(response => response.json())
            // Once the JSON data is available, process it with this function
            .then(data => {
                // Update the button's text to reflect the new upvotes count
                this.innerHTML = `Like (${data.upvotes})`;
            });
        });
    });

    // New code for handling dislike (downvote) button clicks
    document.querySelectorAll('.btn-dislike').forEach(function (button) {
        // Add a click event listener to each 'btn-dislike'
        button.addEventListener('click', function () {
            // Get the comment ID from the data-comment-id attribute
            var commentId = this.getAttribute('data-comment-id');
            // Get the CSRF token from the hidden input field in the 
            // comment form
            var csrfToken = document.querySelector(
                '[name=csrfmiddlewaretoken]').value;
            // Send an AJAX POST request to the downvote URL for the 
            // specified comment ID
            fetch(`/comment/downvote/${commentId}/`, {
                // Specify that the request method is POST
                method: 'POST',
                // Set the request headers
                headers: {
                    // Indicate that the request body contains JSON
                    'Content-Type': 'application/json',
                    // Include the CSRF token in the headers for security
                    'X-CSRFToken': csrfToken,
                },
            })
            // Handle the response from the fetch request and parse it as JSON
            .then(response => response.json())
            // Once the JSON data is available, process it with this function
            .then(data => {
                // Update the button's text to reflect the new downvotes count
                this.innerHTML = `Dislike (${data.downvotes})`;
            });
        });
    });
});
