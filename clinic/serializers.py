from rest_framework import serializers
from .models import *
from accounts.models import Patient, UserAccount
class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

        


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    treatment = TreatmentSerializer()  # Include nested treatment data
    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient(self, obj):
        return {
            "firstName": obj.patient.user.firstname,
            "lastName": obj.patient.user.lastname,
            # Add more fields if needed
        }
    
    
class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ['name', 'direction', 'quantity', 'unit_price', 'total_price']

class PrescriptionSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    drugs = DrugSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'date_prescribed', 'drugs']
        read_only_fields = ['date_prescribed']

    def get_patient(self, obj):
        return {
            "firstName": obj.patient.user.firstname,
            "lastName": obj.patient.user.lastname,
            # Add more fields if needed
        }
    
    def get_doctor(self, obj):
        return {
            "firstName": obj.doctor.user.firstname,
            "lastName": obj.doctor.user.lastname,
            # Add more fields if needed
        }

    def create(self, validated_data):
        drugs_data = validated_data.pop('drugs')
        prescription = Prescription.objects.create(**validated_data)
        for drug_data in drugs_data:
            Drug.objects.create(prescription=prescription, **drug_data)
        return prescription