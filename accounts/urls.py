from django.urls import path
from .views import *

urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'), 
    path('signout/', SignOutView.as_view(), name='signout'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('patients/', list_patients, name='patient_list'),  
    path('patients/signup/', create_patient, name='create_patient'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
    path('staff/', list_staff, name='staff_list'),
    path('staff/create/', create_staff, name='create_staff'),
    path('doctors/', list_doctors, name='doctor_list'),
    
    
]
