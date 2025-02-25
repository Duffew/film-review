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

# Local application-specific imports
from .models import Review, Comment
from .forms import CommentForm


# Create your views here.

class ReviewList(generic.ListView):
    queryset = Review.objects.filter(status=1).order_by("-created_on")
    template_name = "review/index.html"
    paginate_by = 9


def review_detail(request, slug):
    """
    Display an individual :model:`review.Review`.

    **Context**

    ``review``
        An instance of :model:`review.Review`.
    **Template:**

    :template:`review/review_detail.html`
    """
    queryset = Review.objects.filter(status=1)
    review = get_object_or_404(queryset, slug=slug)
    path = "review/review_detail.html"
    all_comments = review.comments.all().order_by("-created_on")
    comments = all_comments.filter(parent__isnull=True)
    comment_count = review.comments.filter(approved=True).count()

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.review = review
            if 'parent' in request.POST:
                parent_id = request.POST.get('parent')
                comment.parent_id = parent_id if parent_id else None
            comment.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Comment submitted and awaiting approval'
            )

    comment_form = CommentForm()
    context = {
        "review": review,
        "comments": comments,
        "comment_count": comment_count,
        "comment_form": comment_form,
    }

    return render(
        request,
        path,
        context
    )


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

    Redirects to the review detail page after the comment is successfully edited.
    """
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            edited_comment = form.save(commit=False)
            edited_comment.approved = False
            edited_comment.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Comment updated successfully and is awaiting approval'
            )
            return HttpResponseRedirect(reverse('review_detail', kwargs={'slug': slug}))
    else:
        form = CommentForm(instance=comment)

    path = 'review/edit_comment.html'
    context = {
        "form": form,
        "slug": slug,
        "comment": comment,
    }

    return render(
        request,
        path,
        context
    )


@login_required
def delete_comment(request, slug, comment_id):
    review = get_object_or_404(Review, slug=slug)
    comment = get_object_or_404(Comment, id=comment_id, review=review)

    if comment.author != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect('review_detail', slug=slug)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Your comment has been deleted.")
        return redirect('review_detail', slug=slug)

    return redirect('review_detail', slug=slug)