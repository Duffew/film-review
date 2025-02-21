# Import path to define URL patterns
from django.urls import path

# Import views from the current package
from . import views


urlpatterns = [
    # Define a urlpattern for ReviewList with the name 'home'
    # Map the root URL to the ReviewList view, naming it 'home'
    path('', views.ReviewList.as_view(), name='home'),

    # Define a urlpattern for review_detail with the name 'review_detail'
    # This pattern enables the slug for each review to become part of the URL
    path('<slug:slug>/', views.review_detail, name="review_detail"),

    # Use url paths for voting as we are changing the state of the comment
    # object and need instant feedback on that update - Separate URLs allow 
    # these actions to be handled via AJAX requests.
    # Add the URL for upvoting a comment
    path('comment/upvote/<int:comment_id>/', views.upvote_comment, 
         name='upvote_comment'),
    
    # Add the URL for downvoting a comment
    path('comment/downvote/<int:comment_id>/', views.downvote_comment, 
         name='downvote_comment'),

    # Define a urlpattern for editing a comment with the name 'edit_comment'
    # This pattern uses both the slug for the review and the comment_id 
    # to identify the comment
    path('<slug:slug>/edit-comment/<int:comment_id>/', views.edit_comment, 
         name='edit_comment'),
]
