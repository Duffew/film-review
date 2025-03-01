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
    """Custom admin configuration for the Review model."""
    # Define how the list of film reviews displays
    list_display = ('film_title', 'slug', 'author', 'created_on', 'status')
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


# Define and register a class to tailor how the admin panel displays.
# Use @admin.register decorator to register the class
@admin.register(Comment)
# Define a class that takes imported SummernoteModelAdmin as a parameter
class CommentAdmin(SummernoteModelAdmin):
    """Custom admin configuration for the Comment model."""
    # Define the list of how the comments display in the panel
    list_display = ('content', 'author', 'created_on', 'approved')
    # Define the quick filters to narrow searches by approved, author and
    # when created
    list_filter = ('approved', 'author', 'created_on')
    # Display the list of comments by most recent first
    ordering = ('-created_on',)
