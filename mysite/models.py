from django.db import models
from django.contrib.auth.models import User

# Post Model
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()  # This is the field for post content
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.date}"

# User Profile Model (Optional, if you want to extend user profiles)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()  # Chat message or text
    pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"Chat by {self.user.username} on {self.created_at}"