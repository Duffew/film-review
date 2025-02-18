from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Review

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
    comments = review.comments.all().order_by("-created_on")
    # Count the number of approved comments associated with the review
    comment_count = review.comments.filter(approved=True).count()
    # Context dictionary containing review, comments and comment_count objects
    context = {
        "review": review,
        "comments": comments,
        "comment_count": comment_count
        }


    # Render the 'review_detail.html' template with the given context
    return render(
        request,  # The current HttpRequest object
        path,  # The path to the template to be rendered
        context  # The context dictionary containing the review object
    )
