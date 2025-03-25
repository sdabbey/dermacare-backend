from django.db import models
from accounts.models import UserAccount
from django.utils import timezone
# Create your models here.


class SkinAnalysis(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)  # Link each analysis to a user
    image = models.ImageField(upload_to="skin_analysis/")
    result = models.TextField(blank=True, null=True)  # AI-detected condition
    confidence = models.FloatField(blank=True, null=True)  # Confidence score
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.firstname} - {self.result if self.result else 'Pending'}"