from rest_framework import serializers
from .models import UserAccount, Patient, Staff
from django.contrib.auth.hashers import make_password
from clinic.serializers import AppointmentSerializer
from clinic.models import Appointment
class UserAccountSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = UserAccount
        fields = ['firstname', 'lastname', 'email', 'password', 'password_confirm', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)
        return super().create(validated_data)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['user', 'gender', 'date_of_birth', 'contact_number', 'address', 'work', 'height', 'ssn']


class PatientListSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'gender', 'date_of_birth', 'contact_number', 'address', 'work', 'height', 'ssn', 'status', 'reg_date']





class StaffSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    avatar = serializers.SerializerMethodField()
    appointments = AppointmentSerializer(many=True, required=False)
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {
            'avatar': {'required': True},
            
        }
    
    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
   
    
class DoctorSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()
    avatar = serializers.SerializerMethodField()
    appointments = AppointmentSerializer(many=True, read_only=True)
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {
            'avatar': {'required': True}
        }
    
    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None