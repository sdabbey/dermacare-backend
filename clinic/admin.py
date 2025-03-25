from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Drug)
admin.site.register(Treatment)