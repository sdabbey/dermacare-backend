from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import *
from .serializers import *
from django.http import JsonResponse

# Treatments 
@api_view(['POST'])
@permission_classes([AllowAny])
def create_treatment(request):
    treatment_data = request.data

    # Serialize the treatment data
    treatment_serializer = TreatmentSerializer(data=treatment_data)
    
    if treatment_serializer.is_valid():
        try:
            with transaction.atomic():
                # Create the treatment
                treatment_serializer.save()
                return Response({'message': 'Treatment created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(treatment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
@api_view(['GET'])
@permission_classes([AllowAny])
def list_treatments(request):
    treatments = Treatment.objects.all()
    serializer = TreatmentSerializer(treatments, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def treatment_count(request):
    count = Treatment.objects.count()
    return Response({'count': count})

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_treatment(request, id):
    try:
        treatment = Treatment.objects.get(id=id)
        treatment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Treatment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


# Appointments
@api_view(['POST'])
@permission_classes([AllowAny])
def create_appointment(request):
    try:
        # Extract patient and treatment data from the request
        patient_data = request.data.get('patient')
        treatment_data = request.data.get('treatment')
        staff_data = request.data.get('staff')
        appointment_date = request.data.get('appointment_date')
        # Assuming patient_data contains the patient's ID or some unique identifier
        if not patient_data or not treatment_data:
            return Response({"detail": "Patient and treatment data are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the patient and treatment instances from the database
        patient = Patient.objects.get(id=patient_data)  # Use the appropriate field to retrieve the patient
        treatment = Treatment.objects.get(id=treatment_data)  # Use the appropriate field to retrieve the treatment
        staff = Staff.objects.get(id=staff_data)
        # Create the Appointment instance
        appointment = Appointment.objects.create(
            patient=patient,
            treatment=treatment,
            staff=staff,
            appointment_date=appointment_date,
            price=treatment.price
        )

        staff.appointments.add(appointment)
        staff.save()
        # Serialize the appointment for the response
        return Response({"detail": "Appointment created successfully."}, status=status.HTTP_201_CREATED)
    
    except Patient.DoesNotExist:
        return Response({"detail": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Treatment.DoesNotExist:
        return Response({"detail": "Treatment not found."}, status=status.HTTP_404_NOT_FOUND)

    except Staff.DoesNotExist:
        return Response({"detail": "Staff member not found."}, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def list_appointments(request):
    appointments = Appointment.objects.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


#Prescriptions
@api_view(['POST'])
@permission_classes([AllowAny])
def create_prescription(request):
    try:
        data = request.data
        
        # Extract and validate doctor and patient
        doctor_id = data.get('doctor')
        patient_id = data.get('patient')

        if not doctor_id or not patient_id:
            return JsonResponse({'error': 'Doctor and Patient fields are required.'}, status=400)
        
        try:
            doctor = Staff.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except (Staff.DoesNotExist, Patient.DoesNotExist) as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Begin atomic transaction
        with transaction.atomic():
            # Create the Prescription
            prescription = Prescription.objects.create(doctor=doctor, patient=patient)
            
            # Extract and create Drug objects
            drugs_data = data.get('prescriptions', [])
            for drug_data in drugs_data:
                Drug.objects.create(
                    prescription=prescription,
                    name=drug_data['name'],
                    direction=drug_data['direction'],
                    quantity=drug_data['quantity'],
                    unit_price=drug_data['unit_price'],
                    total_price=drug_data['total_price']
                )
        
        return JsonResponse({'message': 'Prescription created successfully'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_prescriptions(request):
    prescriptions = Prescription.objects.all()
    serializer = PrescriptionSerializer(prescriptions, many=True)
    return Response(serializer.data)