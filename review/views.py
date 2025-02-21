# Standard library imports
# (none in this example, but place them here if any)

# Third-party imports
# Import render to render templates
# Import get_object_or_404 to retrieve objects or return 404 error if not found
from django.shortcuts import render, get_object_or_404
# Import reverse to reverse URL patterns
from django.urls import reverse
# Import generic for class-based views
from django.views import generic
# Import messages to display messages to users
from django.contrib import messages
# Import JsonResponse to send JSON responses from views - up and down votes
# Import HttpResponseRedirect to enable URL redirects - editing and deleting
from django.http import JsonResponse, HttpResponseRedirect
# Import require_POST to restrict view to POST requests only
from django.views.decorators.http import require_POST
# Import login_required to restrict view to authenticated users only
from django.contrib.auth.decorators import login_required

# Local application-specific imports
# Import models required for views
from .models import Review, Comment
# Import forms required for views
from .forms import CommentForm


# Create your views here.

class ReviewList(generic.ListView):
    # Define the queryset as 'all objects' in the Review model shown in order
    # of newest first
    queryset = Review.objects.all().order_by("-created_on")
    # Specify the html template to be used for rendering the view
    template_name = "review/index.html"
    paginate_by = 9


# Define a function-based view for displaying the details of a single 
# review with the following parameters:
# - request: The current HttpRequest object containing all the information 
# about the client's request
# - slug: A unique identifier used to retrieve the specific review object 
# from the database's Review model
def review_detail(request, slug):
    """
    Display an individual :model:`review.Review`.

    **Context**

    ``review``
        An instance of :model:`review.Review`.

    **Template:**

    :template:`review/review_detail.html`
    """

    # Create a QuerySet of Review objects that have a status of 1 (published)
    queryset = Review.objects.filter(status=1)
    # Get a single Review object from the QuerySet using the review slug, 
    # or return a 404 error if the object does not exist
    review = get_object_or_404(queryset, slug=slug)
    # The path to the template to be rendered
    path = "review/review_detail.html"
    # Retrieve and order all comments associated with the review, 
    # sorting them by the most recently created
    all_comments = review.comments.all().order_by("-created_on")
    # Filter to include only top-level comments (those without a parent)
    comments = all_comments.filter(parent__isnull=True)
    # Count the number of approved comments associated with the review
    comment_count = review.comments.filter(approved=True).count()
    
    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of CommentForm with the POST data
        comment_form = CommentForm(data=request.POST)
        # Check if the form data is valid
        if comment_form.is_valid():
            # Create a comment object but do not save it to the database yet
            comment = comment_form.save(commit=False)
            # Set the author of the comment to the current user
            comment.author = request.user
            # Associate the comment with the current review
            comment.review = review
            # Check if the 'parent' key is present in the POST data indicating
            # a thread
            if 'parent' in request.POST:
                # Retrieve the parent ID from the POST data
                parent_id = request.POST.get('parent')
                # Set the parent_id of the comment if it exists, 
                # otherwise set it to None
                comment.parent_id = parent_id if parent_id else None
            # Save the comment to the database
            comment.save()
            # Add a message to the messages framework
            messages.add_message(
                request,  # The current HttpRequest object
                messages.SUCCESS,  # Level of the message (SUCCESS in this case)
                'Comment submitted and awaiting approval'  # The message text 
                )

   
    # Create an instance of the CommentForm class to handle user input 
    # for the Comment model 
    comment_form = CommentForm()
    # Context dictionary containing review, comments, comment_count and 
    # comment_form objects
    context = {
        "review": review,
        "comments": comments,  # Pass only top-level comments to the template
        "comment_count": comment_count,
        "comment_form": comment_form,
        }


    # Render the 'review_detail.html' template with the given context
    return render(
        request,  # The current HttpRequest object
        path,  # The path to the template to be rendered
        context  # The context dictionary containing the review object
    )


@require_POST  # Ensure the view only handles POST requests
@login_required  # Ensure the user is authenticated before accessing the view
def upvote_comment(request, comment_id):
    # Retrieve the comment object by its ID, or return a 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id)
    # Increment the upvotes count for the comment
    comment.upvotes += 1
    # Save the updated comment object to the database
    comment.save()
    # Return a JSON response with the updated upvotes count
    return JsonResponse({'upvotes': comment.upvotes})

@require_POST  # Ensure the view only handles POST requests
@login_required  # Ensure the user is authenticated before accessing the view
def downvote_comment(request, comment_id):
    # Retrieve the comment object by its ID, or return a 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id)
    # Increment the downvotes count for the comment
    comment.downvotes += 1
    # Save the updated comment object to the database
    comment.save()
    # Return a JSON response with the updated downvotes count
    return JsonResponse({'downvotes': comment.downvotes})


# Ensure that the user is authenticated before accessing this view
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

    Redirects to the review detail page after the comment is 
    successfully edited.
    """
    # Get the comment object to be edited or return a 404 error if not found
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of CommentForm with the POST data and the existing 
        # comment instance
        form = CommentForm(request.POST, instance=comment)
        # Check if the form data is valid
        if form.is_valid():
            # Save the edited comment to the database, setting approval to False
            edited_comment = form.save(commit=False)
            edited_comment.approved = False
            edited_comment.save()
            # Add a success message to the messages framework
            messages.add_message(
                request,  # The current HttpRequest object
                messages.SUCCESS,  # Level of the message (SUCCESS in this case)
                'Comment updated successfully and is awaiting approval'
            )
            # Redirect to the review detail page of the associated review 
            # using the slug
            return HttpResponseRedirect(reverse('review_detail', kwargs={
                'slug': slug}))
    else:
        # Create an instance of CommentForm with the existing comment 
        # instance for GET request
        form = CommentForm(instance=comment)

    # Path to the template to be rendered
    path = 'review/edit_comment.html'
    
    # Context dictionary containing the form object
    context = {
        "form": form,
        "slug": slug,
        "comment": comment,
    }

    # Render the 'edit_comment.html' template with the given context
    return render(
        request,  # The current HttpRequest object
        path,  # The path to the template to be rendered
        context  # The context dictionary containing the form object
    )
