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

     # Define a urlpattern for editing a comment with the name 'edit_comment'
     # This pattern uses both the slug for the review and the comment_id
     # to identify the comment
     path('<slug:slug>/edit-comment/<int:comment_id>/', views.edit_comment,
          name='edit_comment'),

     # Define urlpattern for deleting a comment with the name 'delete_comment'
     # This pattern uses both the slug for the review and the comment_id
     # to identify the comment
     path('<slug:slug>/delete-comment/<int:comment_id>/', views.delete_comment,
          name='delete_comment'),
]
