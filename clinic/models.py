from django.db import models
from accounts.models import Patient, Staff
# Create your models here.

class Treatment(models.Model):
    VISIT_CHOICES = (
        ('multiple', 'Multiple'),
        ('single', 'Single')
    )
    
    name = models.CharField(db_column='treatment_name', max_length=200)
    price = models.IntegerField(db_column='price')
    estimated_duration = models.TextField(db_column='estimated_duration')
    visit_type = models.CharField(db_column='visit_type', choices=VISIT_CHOICES, max_length=20)

    class Meta:
        managed = True
        db_table = 'treatments'

    def __str__(self):
        return f"Treatment: {self.name}"

class Appointment(models.Model):
    
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='appointments')
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE, related_name='appointments_set')
    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField(blank=True, null=True)
    price= models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'appointments'

    def __str__(self):
        return f"Appointment {self.pk} for {self.staff.user.firstname} {self.staff.user.lastname} with {self.patient.user.firstname} {self.patient.user.lastname} on {self.appointment_date}"


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='prescriptions')
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor} on {self.date_prescribed}"

class Drug(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='drugs')
    name = models.CharField(max_length=255)
    direction = models.TextField()
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.quantity}) for {self.prescription.patient}"

# class Exams(models.Model):
#     examid = models.AutoField(db_column='examid', primary_key=True)
#     patientid = models.ForeignKey(
#         'Patients', models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     examname = models.CharField(
#         db_column='examname', max_length=100, blank=True, null=True)
#     examdate = models.DateField(db_column='examdate', blank=True, null=True)
#     result = models.TextField(db_column='result', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'exams'


# class Images(models.Model):
#     imageid = models.AutoField(db_column='imageid', primary_key=True)
#     patientid = models.ForeignKey(
#         'Patients', models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     imagename = models.CharField(
#         db_column='imagename', max_length=255, blank=True, null=True)
#     imagedescription = models.TextField(
#         db_column='imagedescription', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'images'


# class Insurance(models.Model):
#     insuranceid = models.AutoField(db_column='insuranceid', primary_key=True)
#     patientid = models.ForeignKey(
#         'Patients', models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     insuranceprovider = models.CharField(
#         db_column='insuranceprovider', max_length=100, blank=True, null=True)
#     policynumber = models.CharField(
#         db_column='policynumber', max_length=50, blank=True, null=True)
#     expirationdate = models.DateField(
#         db_column='expirationdate', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'insurance'


# class Labresults(models.Model):
#     labresultid = models.AutoField(db_column='labresultid', primary_key=True)
#     examid = models.ForeignKey(
#         Exams, models.DO_NOTHING, db_column='examid', blank=True, null=True)
#     testname = models.CharField(
#         db_column='testname', max_length=100, blank=True, null=True)
#     resultvalue = models.CharField(
#         db_column='resultvalue', max_length=50, blank=True, null=True)
#     resultdate = models.DateField(
#         db_column='resultdate', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'labresults'


# class Medicalhistory(models.Model):
#     historyid = models.AutoField(db_column='historyid', primary_key=True)
#     patientid = models.ForeignKey(
#         'Patients', models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     conditionname = models.CharField(
#         db_column='conditionname', max_length=100, blank=True, null=True)
#     diagnosisdate = models.DateField(
#         db_column='diagnosisdate', blank=True, null=True)
#     description = models.TextField(
#         db_column='description', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'medicalhistory'





# class Prescriptions(models.Model):
#     prescriptionid = models.AutoField(
#         db_column='prescriptionid', primary_key=True)
#     patientid = models.ForeignKey(
#         Patients, models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     medicationname = models.CharField(
#         db_column='medicationname', max_length=100, blank=True, null=True)
#     dosage = models.CharField(
#         db_column='dosage', max_length=50, blank=True, null=True)
#     prescriptiondate = models.DateField(
#         db_column='prescriptiondate', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'prescriptions'


# class Visits(models.Model):
#     visitid = models.AutoField(db_column='visitid', primary_key=True)
#     patientid = models.ForeignKey(
#         Patients, models.DO_NOTHING, db_column='patientid', blank=True, null=True)
#     visitdate = models.DateField(db_column='visitdate', blank=True, null=True)
#     purpose = models.CharField(
#         db_column='purpose', max_length=255, blank=True, null=True)
#     notes = models.TextField(db_column='notes', blank=True, null=True)
#     reason_of_admittance = models.CharField(
#         db_column='reason_of_admittance', max_length=255, blank=True, null=True)
#     hospital = models.CharField(
#         db_column='hospital', max_length=255, blank=True, null=True)
#     hospital_exit = models.DateField(
#         db_column='hospital_exit', blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'visits'
