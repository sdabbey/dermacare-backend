from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .serializers import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from django.contrib.auth import authenticate
from .models import *

@api_view(['POST'])
@permission_classes([AllowAny])
def create_patient(request):
    user_data = request.data.get('user')
    if not user_data:
        return Response({'non_field_errors': 'User data not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    patient_data = request.data.copy()
    
    user_serializer = UserAccountSerializer(data=user_data)
    
    if user_serializer.is_valid():
        try:
            with transaction.atomic():
                # Create the user
                user = user_serializer.save()
                
                # Update patient data to include the user reference
                patient_data['user'] = user.id
                patient_serializer = PatientSerializer(data=patient_data)
                
                if patient_serializer.is_valid():
                    patient_serializer.save()
                    return Response({'message': 'User and patient created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    # Rollback the user creation if patient creation fails
                    user.delete()
                    return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET'])
@permission_classes([AllowAny])  # Adjust permissions as needed
def list_patients(request):
    try:
        # Retrieve all patients from the database
        patients = Patient.objects.all()
        
        # Serialize the patient data
        serializer = PatientListSerializer(patients, many=True)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle any unexpected errors
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PatientDetailView(RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientListSerializer
    lookup_field = 'pk'  # Use patient ID from URL   

@api_view(['POST'])
def create_staff(request):
    # Extract the user data and parse it
    user_data = request.data.get('user')
    if user_data:
        import json
        user_data = json.loads(user_data)  # Convert string to dictionary
    else:
        return Response({'non_field_errors': 'User data not provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Extract the file (avatar) from the request
    avatar = request.FILES.get('avatar')

    # Prepare staff data including the avatar
    staff_data = request.data.copy()
    staff_data['avatar'] = avatar

    # Initialize serializers
    user_serializer = UserAccountSerializer(data=user_data)
    
    if user_serializer.is_valid():
        try:
            with transaction.atomic():
                # Save the user
                user = user_serializer.save()
                print(user.id)
                # Update staff data to include the user reference
                staff_data['user'] = user.id
                staff = Staff.objects.create(
                    user=user,
                    avatar=avatar,
                    group=staff_data.get('group'),
                    date_of_birth=staff_data.get('date_of_birth'),
                    gender=staff_data.get('gender'),
                    work_status=staff_data.get('work_status'),
                    specialization=staff_data.get('specialization'),
                    assigned_treatment=staff_data.get('assigned_treatment'),
                    working_days=staff_data.get('working_days'),
                    
                    address=staff_data.get('address'),
                    contact_number=staff_data.get('contact_number'),
                   
                    
                )

                return Response({'message': 'User and staff created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def list_staff(request):
    try:
        staff = Staff.objects.all()
        serializer = StaffSerializer(staff, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_doctors(request):
    try:
        staff = Staff.objects.filter(group__in=['medical', 'allied-health'])
        serializer = StaffSerializer(staff, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignInView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

      
        # Authenticate user
        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Create or get the token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'role': user.role
            })
    
class SignOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()  # Delete the token
        except (AttributeError, Token.DoesNotExist):
            pass  # Token might not exist
        
        return Response({"message": "Successfully logged out."})
    

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserAccountSerializer(user)
        return Response(serializer.data)