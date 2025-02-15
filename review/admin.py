from django.contrib import admin
# Import the Review model from the same directory
from .models import Review, Comment

# Register your models here.
# Register the Review model to enable review management from the admin panel
admin.site.register(Review)
# Register the Comment model to enable review management from the admin panel
admin.site.register(Comment)
