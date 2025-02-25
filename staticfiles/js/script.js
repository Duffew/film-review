/**
 * This script handles various event listeners for comment functionality,
 * including showing and hiding nested comment forms, and deleting comments
 * Within this script, we use `const` to declare variables that should not be 
 * reassigned after their initial value is set. Using `const` in local contexts 
 * helps to:
 * 1. Ensure variable values remain constant within their scope,
 * 2. Enhance code readability by signaling that these variables won't change,
 * 3. Prevent accidental reassignments which can lead to bugs.
 */

// Wait until the DOM (Document Object Model) is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Select all elements with the class 'reply-btn' and iterate over them
    document.querySelectorAll('.reply-btn').forEach(function (button) {
        // Add a click event listener to each 'reply-btn'
        button.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent the default action of the link
            // Get the value of the 'data-parent' attribute from the clicked button
            const parentId = this.getAttribute('data-parent');
            // Find the closest comment container and the nested comment form within it
            const parentComment = this.closest('.comments');
            const nestedForm = parentComment.querySelector('.nested-comment-form');
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


    // Delete modal logic
    // Select all elements that have the attribute 'data-bs-target' with the 
    // value '#deleteModal' and iterate over them
    document.querySelectorAll('[data-bs-target="#deleteModal"]').forEach(
        function (button) {
            // Add a click event listener to each button
            button.addEventListener('click', function () {
            // Retrieve the comment ID from the 'data-comment-id' attribute of 
            // the clicked button
            const commentId = this.getAttribute('data-comment-id');
            // Retrieve the comment slug from the 'data-comment-slug' attribute 
            // of the clicked button
            const commentSlug = this.getAttribute('data-comment-slug');
            // Get the form element with the ID 'deleteCommentForm'
            const form = document.getElementById('deleteCommentForm');
            // Construct the action URL using the comment slug and comment ID
            const actionUrl = `/${commentSlug}/delete-comment/${commentId}/`;
            // Set the 'action' attribute of the form to the constructed URL
            form.setAttribute('action', actionUrl);
        });
    });
});
