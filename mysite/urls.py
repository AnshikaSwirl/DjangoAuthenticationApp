
from django.contrib import admin
from django.urls import path, include
from .views import index, registration_view
from django.conf import settings
from django.conf.urls.static import static
from .views import get_user_chats, get_chat_pdf
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('posts/', views.get_user_chats, name='get_posts'),
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("",index, name="index"),
    path('register/', views.registration_view, name='register'),
    
    path('api/chats/pdf/<int:chat_id>/', get_chat_pdf, name='get_chat_pdf'),
    # Fetch user chats endpoint
    path('api/chats/<int:user_id>/', get_user_chats, name='get_user_chats'),

    
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)