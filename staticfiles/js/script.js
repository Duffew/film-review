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
})   