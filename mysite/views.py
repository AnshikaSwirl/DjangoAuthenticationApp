from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.shortcuts import redirect,render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Chat
from .serializers import ChatSerializer
from django.http import JsonResponse
from .models import Chat
from django.contrib.auth.models import User
from django.http import FileResponse
from .models import Chat

@login_required
def get_chat_pdf(request, chat_id):
    chat = Chat.objects.get(id=chat_id, user=request.user)
    response = FileResponse(chat.pdf_file.open(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="chat_{}.pdf"'.format(chat_id)
    return response

@login_required
def get_user_chats(request, user_id):
    # Filter chats that only belong to the logged-in user
    user_chats = Chat.objects.filter(user=request.user)
    return render(request, 'chats.html', {'chats': user_chats})

@login_required
def welcome_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the current logged-in user as the author
            post.save()
            return redirect('index')  # Redirect back to the homepage after submission
    else:
        form = PostForm()

    posts = Post.objects.all().order_by('-created_at')  # Retrieve all posts, ordered by creation time
    return render(request, 'index.html', {'form': form, 'posts': posts})
@login_required
def create_chat(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        pdf_file = request.FILES['pdf_file'] if 'pdf_file' in request.FILES else None
        Chat.objects.create(user=request.user, title=title, content=content, pdf_file=pdf_file)
        return redirect('get_user_chats', user_id=request.user.id)
    return render(request, 'create_chat.html')
class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=["username","email","password1","password2"]

def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")  # Redirect to the view name, not the template
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})  
# 1. Fetch user's previous chats
@api_view(['GET'])
@login_required
def get_user_chats(request, user_id):
    # Get all chats for a user, ordered by date
    chats = Chat.objects.filter(user_id=user_id).order_by('-created_at')
    
    if not chats.exists():
        return Response({'error': 'No chats found for this user'}, status=status.HTTP_404_NOT_FOUND)
    
    # Serialize the chats
    serializer = ChatSerializer(chats, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


# 2. Fetch the PDF file associated with a chat
@api_view(['GET'])
def get_chat_pdf(request, chat_id):
    # Get the chat based on the chat_id
    chat = get_object_or_404(Chat, id=chat_id)
    
    if not chat.pdf:
        return Response({'error': 'No PDF associated with this chat'}, status=status.HTTP_404_NOT_FOUND)

    # Serve the PDF file
    pdf_url = chat.pdf.url  # This gives the URL of the uploaded PDF file
    return Response({'pdf_url': pdf_url}, status=status.HTTP_200_OK)
def login_view(request):
    if request.method == 'POST':
        # Add your login logic here (e.g., authentication)
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the post's author as the current user
            post.save()
            return redirect('index')  # Redirect to avoid form resubmission
    else:
        form = PostForm()

    # Filter posts so that only the current user's posts are shown
    posts = Post.objects.filter(author=request.user).order_by('-created_at')

    return render(request, 'index.html', {'form': form, 'posts': posts})
