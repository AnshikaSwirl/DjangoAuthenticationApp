from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'text', 'created_at']  # Exclude the pdf field for the chat list
