from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.firstname', read_only=True)  # Include sender's name

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_name', 'content', 'timestamp', 'is_read']

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.firstname', read_only=True)  # Include patient name

    class Meta:
        model = Conversation
        fields = ['id', 'patient', 'patient_name', 'staff_group', 'created_at', 'messages']
