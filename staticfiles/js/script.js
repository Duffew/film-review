// Wait until the DOM (Document Object Model) is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Select all elements with the class 'reply-btn' and iterate over them
    document.querySelectorAll('.reply-btn').forEach(function (button) {
        // Add a click event listener to each 'reply-btn'
        button.addEventListener('click', function (event) {
            event.preventDefault();  // Prevent the default action of the link
            // Get the value of the 'data-parent' attribute from the clicked button
            let parentId = this.getAttribute('data-parent');
            // Find the closest comment container and the nested comment form within it
            let parentComment = this.closest('.comments');
            let nestedForm = parentComment.querySelector('.nested-comment-form');
            // Set the parent ID in the nested form's hidden input field
            nestedForm.querySelector('.parent-id').value = parentId;
            // Toggle the visibility of the nested comment form
            if (nestedForm.style.display === 'block') {
                nestedForm.style.display = 'none';  // Hide the form if it's currently visible
            } else {
                nestedForm.style.display = 'block';  // Show the form if it's currently hidden
            }
        });
    });

    // Delete modal logic
    document.querySelectorAll('[data-bs-target="#deleteModal"]').forEach(function (button) {
        button.addEventListener('click', function () {
            const commentId = this.getAttribute('data-comment-id');
            const commentSlug = this.getAttribute('data-comment-slug');
            const form = document.getElementById('deleteCommentForm');
            const actionUrl = `/${commentSlug}/delete-comment/${commentId}/`;
            form.setAttribute('action', actionUrl);
        });
    });
});
