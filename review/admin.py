from django.contrib import admin
# Import the Review model from the same directory
from .models import Review, Comment
# Import the text editor to be used within the admin panel
from django_summernote.admin import SummernoteModelAdmin

# Define aand register a class  - use @ decorator to indicate class
@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('film_title', 'slug', 'author', 'status')
    search_fields = ['film_title']
    list_filter = ('status',)
    prepopulated_fields = {'slug': ('film_title',)}
    summernote_fields = ('content',)
    ordering = ('-created_on',)

# Register your models here.
# Register the Comment model to enable review management from the admin panel
admin.site.register(Comment)
