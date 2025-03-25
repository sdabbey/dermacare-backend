from django.db import models
from django.utils import timezone
from accounts.models import UserAccount  # Import your user model

class Conversation(models.Model):
    patient = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='patient_conversations', limit_choices_to={'role': 'patient'})
    staff_group = models.CharField(max_length=50, choices=UserAccount.ROLE_CHOICES, default='medical')  # Group of staff
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation between {self.patient.firstname} and {self.staff_group}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.firstname} in {self.conversation}"
