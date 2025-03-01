# Standard library imports
# (none in this example, but place them here if any)

# Third-party imports
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

# Local application-specific imports
from .models import Review, Comment
from .forms import CommentForm


# Create your views here.

# Define a 'ReviewList' class which inherits from Django's generic ListView
class ReviewList(generic.ListView):
    """
    View to display a list of published reviews.

    **Queryset:**

    Filters Review objects with a status of 1 (published),
    annotates each review
    with the count of approved comments, and orders the reviews by the
    'created_on' field in descending order.

    **Template:**

    :template:`review/index.html`

    **Pagination:**

    Displays 6 reviews per page.
    """

    # Set the queryset to filter Review objects with a status of 1 (approved)
    # and annotate each review with a new field 'comment_count' of approved
    # comments, then order the reviews by the 'created_on' field in
    # descending order
    queryset = Review.objects.filter(status=1).annotate(
        comment_count=Count('comments', filter=Q(comments__approved=True))
    ).order_by("-created_on")

    # Specify the template to be used for rendering the list view
    template_name = "review/index.html"

    # Set the number of reviews to be displayed per page
    paginate_by = 6


# Define a function called 'review_detail' that takes a request and a slug
# as parameters
def review_detail(request, slug):
    """
    Display an individual :model:`review.Review`.

    **Context**

    ``review``
        An instance of :model:`review.Review`.
    **Template:**

    :template:`review/review_detail.html`
    """

    # Filter the Review objects to only include those with a status of
    # 1 (published)
    queryset = Review.objects.filter(status=1)

    # Get the review object that matches the given slug or return a
    # 404 error if not found
    review = get_object_or_404(queryset, slug=slug)

    # Specify the path to the template used for rendering the review details
    path = "review/review_detail.html"

    # Get all comments related to the review and order them by creation
    # date in descending order
    all_comments = review.comments.all().order_by("-created_on")

    # Filter the comments to only include top-level comments
    # (those without a parent)
    comments = all_comments.filter(parent__isnull=True)

    # Count the number of approved comments for the review
    comment_count = review.comments.filter(approved=True).count()

    # Check if the request method is POST (indicating form submission)
    if request.method == "POST":
        # Initialize the comment form with the data from the POST request
        comment_form = CommentForm(data=request.POST)
        # Validate the form data
        if comment_form.is_valid():
            # Create a comment object but do not save it to the database yet
            comment = comment_form.save(commit=False)
            # Set the author of the comment to the current user
            comment.author = request.user
            # Associate the comment with the current review
            comment.review = review
            # Check if there is a 'parent' field in the POST data and set the
            # parent_id if present
            if 'parent' in request.POST:
                parent_id = request.POST.get('parent')
                comment.parent_id = parent_id if parent_id else None
            # Save the comment to the database
            comment.save()
            # Add a success message indicating that the comment was submitted
            # and is awaiting approval
            messages.add_message(
                request,
                messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    # Initialize an empty comment form
    comment_form = CommentForm()

    # Create a context dictionary to pass data to the template
    context = {
        "review": review,         # The review object
        "comments": comments,     # Top-level comments
        "comment_count": comment_count,  # Number of approved comments
        "comment_form": comment_form,    # Empty comment form
    }

    # Render the review detail template with the provided context
    return render(
        request,
        path,
        context
    )


# Ensure that the user is logged in before they can edit comments
@login_required
def edit_comment(request, slug, comment_id):
    """
    View to handle the editing of a comment.

    **Parameters:**

    ``request``: HttpRequest object
        The current HttpRequest object containing all the information about
        the client's request.
    ``slug``: str
        The slug of the review to which the comment belongs.
    ``comment_id``: int
        The ID of the comment to be edited.

    **Context:**

    ``form``: CommentForm
        An instance of CommentForm used to display and validate the form data.

    **Template:**

    :template:`review/edit_comment.html`

    **Redirects:**

    Redirects to the review detail page after the comment is edited.
    """
    # Get the comment object with the given id and author, or return a
    # 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    # Check if the request method is POST (indicating form submission)
    if request.method == "POST":
        # Initialize the comment form with the data from the POST request
        # and the existing comment instance
        form = CommentForm(request.POST, instance=comment)
        # Validate the form data
        if form.is_valid():
            # Create the edited comment object but do not save it to the
            # database yet
            edited_comment = form.save(commit=False)
            # Mark the comment as not approved to await moderation
            edited_comment.approved = False
            # Save the edited comment to the database
            edited_comment.save()
            # Add a success message indicating that the comment was updated
            # and is awaiting approval
            messages.add_message(
                request,
                messages.SUCCESS,
                'Comment updated successfully and is awaiting approval'
            )
            # Redirect to the review detail page for the given slug
            return HttpResponseRedirect(reverse('review_detail', kwargs={
                'slug': slug}))
    else:
        # If the request method is not POST, initialize the comment form with
        # the existing comment instance
        form = CommentForm(instance=comment)

    # Specify the path to the template used for rendering the edit comment form
    path = 'review/edit_comment.html'
    # Create a context dictionary to pass data to the template
    context = {
        "form": form,         # The comment form
        "slug": slug,         # The slug of the review
        "comment": comment,   # The comment object
    }

    # Render the edit comment template with the provided context
    return render(
        request,
        path,
        context
    )


# Ensure that the user is logged in before they can delete comments
@login_required
def delete_comment(request, slug, comment_id):
    """
    View to handle the deletion of a comment.

    **Parameters:**

    ``request``: HttpRequest object
        The current HttpRequest object containing all the information about
        the client's request.
    ``slug``: str
        The slug of the review to which the comment belongs.
    ``comment_id``: int
        The ID of the comment to be deleted.

    **Redirects:**

    Redirects to the review detail page after the comment is deleted
    or if the user does not have permission to delete the comment.
    """

    # Get the review object that matches the given slug or return a 404 error
    # if not found
    review = get_object_or_404(Review, slug=slug)
    # Get the comment object with the given id and review, or return a
    # 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id, review=review)

    # Check if the author of the comment is not the current user
    if comment.author != request.user:
        # Add an error message indicating that users can only delete their
        # own comments
        messages.error(request, "You can only delete your own comments.")
        # Redirect to the review detail page
        return redirect('review_detail', slug=slug)

    # Check if the request method is POST (indicating form submission)
    if request.method == 'POST':
        # Delete the comment from the database
        comment.delete()
        # Add a success message indicating that the comment has been deleted
        messages.success(request, "Your comment has been deleted.")
        # Redirect to the review detail page
        return redirect('review_detail', slug=slug)

    # Redirect to the review detail page if the request method is not POST
    return redirect('review_detail', slug=slug)
