# Import views file and path
from . import views
from django.urls import path


urlpatterns = [
    # Define a urlpattern for ReviewList with the name 'home'
    # Map the root URL to the ReviewList view, naming it 'home' 
    path('', views.ReviewList.as_view(), name='home'),
    # Define a urlpattern for review_detail with the name 'review_detail'
    # This pattern will enable the slug for each reveiw to become part of
    # the URL
    path('<slug:slug>/', views.review_detail, name="review_detail"),
]