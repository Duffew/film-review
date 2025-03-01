# Import the Comment model from this directory
from .models import Comment
# Import the forms module from Django
from django import forms


# Define a form class named CommentForm, inheriting from Django's ModelForm
class CommentForm(forms.ModelForm):
    """A form for creating and editing Comment instances."""
    class Meta:
        # Specify the model to be used, in this case, Comment
        model = Comment
        # Define the fields to be included in the form, here it is 'content'
        fields = ('content',)
