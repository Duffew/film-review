from django.shortcuts import render
from django.views import generic
from .models import Review

# Create your views here.

class ReviewList(generic.ListView):
    # Define the queryset as 'all objects' in the Review model shown in order
    # of newest first
    queryset = Review.objects.all().order_by("-created_on")
    # Specify the html template to be used for rendering the view
    template_name = "review/index.html"
    paginate_by = 12