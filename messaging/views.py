from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from accounts.models import UserAccount

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'patient':
            return Conversation.objects.filter(patient=user)
        elif user.role in ['medical', 'nursing', 'administrative']:  # Staff groups
            return Conversation.objects.filter(staff_group=user.role)
        return Conversation.objects.none()

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        conversation = Conversation.objects.get(id=conversation_id)

        # Ensure sender is either the patient or the correct staff group
        if self.request.user.role == 'patient' and self.request.user != conversation.patient:
            return Response({"error": "You can only send messages in your conversations"}, status=403)
        if self.request.user.role in ['medical', 'nursing', 'administrative'] and self.request.user.role != conversation.staff_group:
            return Response({"error": "You can only send messages in your assigned group"}, status=403)

        serializer.save(sender=self.request.user)
