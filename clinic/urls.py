from django.urls import path
from .views import *

urlpatterns = [
    #Treatment endpoints
    path('treatments/', list_treatments, name='treatments'),
    path('treatments/add/', create_treatment, name='add_treatments'),
    path('treatments/count/', treatment_count, name='treatment_count'),  
    path('treatments/<int:id>/', delete_treatment, name='delete_treatment'), 
    #Appointment endpoints
    path('appointments/', list_appointments, name="list_appointments"),
    path('appointments/add/', create_appointment, name='add_appointments'),
    #Prescription endpoints
    path('prescriptions/', list_prescriptions, name="list_prescriptions"),
    path('prescriptions/add/', create_prescription, name="add_prescription")
]
