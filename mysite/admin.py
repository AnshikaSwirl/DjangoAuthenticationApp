from django.contrib import admin
from .models import Post

# Registering the Post model with the admin interface
admin.site.register(Post)
