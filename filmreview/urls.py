"""
URL configuration for filmreview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# Define the URL patterns for the Django application.
# This list contains all the URL configurations, directing requests to the 
# appropriate views.
# # Order alphabetically, with empty string last, then by most detailed first
urlpatterns = [    
    # Include the URL configurations for Django Allauth.
    # This allows handling of account-related paths such as signup, login, 
    # logout, etc., under the 'accounts/' URL.
    path("accounts/", include("allauth.urls")),
    # Define the URL path for the Django admin interfac. This allows access to 
    # the Django admin site where administrators can manage the application.
    path('admin/', admin.site.urls),
    # Include the URL configurations for the django-summernote package.
    # This allows handling of summernote-related paths, enabling the rich text 
    # editor under the 'summernote/' URL.
    path('summernote/', include('django_summernote.urls')),
    # Include the URL configurations for the 'review' app.
    # This allows handling of review-related paths under the base URL.
    path("", include("review.urls"), name='review-urls'),
    
]
