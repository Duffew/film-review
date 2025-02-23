# Import models from django.db to define database schema
from django.db import models
# Import the User model from Django's built-in authentication framework
from django.contrib.auth.models import User


STATUS = ((0, "Draft"), (1, "Published"))
# Create your models here.
class Review(models.Model):
    # Define a field for the film title which must be unique in the database
    film_title = models.CharField(max_length=200, unique=True)

    # Define a slug field to help build urls for each review
    slug = models.SlugField(max_length=200, unique=True)

    # Define an author field which references a foriegn key field type and uses
    # Django's built-in authentication framework 'User' as an argument.
    # Include full deletion of Review instances if the User is deleted.
    # Include a reverse relationship to enable a query set of Review instances 
    # by author.
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='reviews')
    
    # Define a content field for the film review text
    content = models.TextField()

    # Add a field for the director's name
    director = models.CharField(max_length=100)

    # Add a field for the year the film was released; positive integers only
    release_year = models.PositiveIntegerField()

    # Add a field for automatically capturing the date and time of creation
    created_on = models.DateTimeField(auto_now_add=True)

    # Add a status field to help manage draft vs published reviews
    # This will require a STATUS constant defined above
    status = models.IntegerField(choices=STATUS, default=0)

    # Add an optional exceprt field to allow readers to see the start of a
    # review on the list page
    excerpt = models.TextField(blank=True)


    # Add a Meta class to order the film reviews by most recent first when
    # displayed as a list
    class Meta:
        ordering = ["-created_on"]

    # Add a string method to detail how Review instances should be displayed
    def __str__(self):
        return f"{self.film_title} | Reviewed by {self.author}"
    

# Create a Comments model to manage comments on the film reviews
class Comment(models.Model):
    # Create a many-to-one relationship to the Review model that deletes if
    # the film review is deleted
    review = models.ForeignKey(Review, on_delete=models.CASCADE, 
                               related_name="comments")
    
    # Reference the User model for the author of the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # Capture the content of the comment using TextField
    content = models.TextField()

    # Add an approved field to enable Site Admin to approve the comment
    approved = models.BooleanField(default=False)

    # Add a field to automatically capture the date and time 
    # the comment was created
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Create a self-referential foreign key to enable threaded comments
    parent = models.ForeignKey('self', null=True, blank=True, 
                               related_name='replies', on_delete=models.CASCADE)

    
    # Add metadata to enable comments to show in order of oldest first
    # by default.
    class Meta:
        ordering = ["created_on"]

    
    # Add a string method to define how the comment should read as a string. 
    def __str__(self):
        return f"{self.author} wrote: {self.content}"
    