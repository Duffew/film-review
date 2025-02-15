# Import views file and path
from . import views
from django.urls import path


urlpatterns = [
    # Define a urlpattern for ReviewList with the name 'home'
    # Map the root URL to the ReviewList view, naming it 'home' 
    path('', views.ReviewList.as_view(), name='home'),
]