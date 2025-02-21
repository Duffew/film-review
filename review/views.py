from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Review, Comment
from .forms import CommentForm
# Import the messages framework from Django's contrib package
from django.contrib import messages

# Imports required for up and downvoting comments
# Import JsonResponse to send JSON responses from views
from django.http import JsonResponse
# Import require_POST to restrict view to POST requests only
from django.views.decorators.http import require_POST
# Import login_required to restrict view to authenticated users only
from django.contrib.auth.decorators import login_required

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
            # 
            if 'parent' in request.POST:
                parent_id = request.POST.get('parent')
                comment.parent_id = parent_id if parent_id else None
            # Save the comment to the database
            comment.save()
            # Add a message to the messages framework
            messages.add_message(
                request,  # The current HttpRequest object
                messages.SUCCESS,  # The level of the message (SUCCESS in this case)
                'Comment submitted and awaiting approval'  # The message text to be displayed to the user
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

