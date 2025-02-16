from django.contrib import admin
# Import the Review model from the same directory
from .models import Review, Comment
# Import the text editor to be used within the admin panel
from django_summernote.admin import SummernoteModelAdmin

# Define and register a class to tailor how the admin panel displays.
# Use @admin.register decorator to register the class
# Tuples with one element need a trailing comma to define them as tuples 
# rather than strings. Tuples with multiple entries do not need a trailing 
# comma after the last element as context defines them as tuples.
@admin.register(Review)
# Define a class that takes imported SummernoteModelAdmin as a parameter
class ReviewAdmin(SummernoteModelAdmin):
    # Define how the list of film reviews displays
    list_display = ('film_title', 'slug', 'author', 'status', 'created_on')
    # Add a search field to find films by title
    search_fields = ['film_title']
    # Add quick filters to narrow searches by status, author and date created
    list_filter = ('status', 'author', 'created_on')
    # Prepopulate the slug field - will help with making site URLs more search
    # engine friendly. Derived from film title
    prepopulated_fields = {'slug': ('film_title',)}
    # Apply the summernote text editor to the admin interface for 
    # creating reviews and excerpts
    summernote_fields = ('content', 'excerpt')
    # List the film reviews in order of most recent first
    ordering = ('-created_on',)


# Register your models here.
# Register the Comment model to enable review management from the admin panel
admin.site.register(Comment)
