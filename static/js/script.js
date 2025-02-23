document.addEventListener('DOMContentLoaded', function () {
    let editModal = document.getElementById('editModal');
    if (editModal) {
        editModal.addEventListener('show.bs.modal', function (event) {
            let button = event.relatedTarget;
            let commentId = button.getAttribute('data-comment-id');
            let commentContent = document.getElementById(`comment${commentId}`).innerText;
            let form = document.getElementById('editCommentForm');
            let actionUrl = form.getAttribute('action').replace('__id__', commentId);
            form.setAttribute('action', `edit_comment/${commentId}`);
            document.getElementById('commentContent').value = commentContent;
        });
    }

    let deleteModal = document.getElementById('deleteModal');
    if (deleteModal) {
        deleteModal.addEventListener('show.bs.modal', function (event) {
            let button = event.relatedTarget;
            let commentId = button.getAttribute('data-comment-id');
            let commentSlug = button.getAttribute('data-comment-slug');
            let form = document.getElementById('deleteCommentForm');
            let actionUrl = form.getAttribute('action').replace('__slug__', commentSlug).replace('__id__', commentId);
            form.setAttribute('action', actionUrl);
        });
    }

    document.querySelectorAll('.reply-btn').forEach(function (button) {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            let parentId = this.getAttribute('data-parent');
            let parentComment = this.closest('.comments');
            let nestedForm = parentComment.querySelector('.nested-comment-form');
            nestedForm.querySelector('.parent-id').value = parentId;
            nestedForm.style.display = (nestedForm.style.display === 'block') ? 'none' : 'block';
        });
    });
});
