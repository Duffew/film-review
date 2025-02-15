from django.shortcuts import render
from django.views import generic
from .models import Review

# Create your views here.

class ReviewList(generic.ListView):
    # Define the queryset as 'all objects' in the Review model
    queryset = Review.objects.all()
    # Specify the html template to be used for rendering the view
    template_name = "review_list.html"