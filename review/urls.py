# Import views file and path
from . import views
from django.urls import path


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
]