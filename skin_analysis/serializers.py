from rest_framework import serializers
from .models import SkinAnalysis
from accounts.serializers import UserAccountSerializer

class SkinAnalysisSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    class Meta:
        model = SkinAnalysis
        fields = '__all__'
        read_only_fields = ['user', 'result', 'confidence']
