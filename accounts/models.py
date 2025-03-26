from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserAccountManager(BaseUserManager):
    def create_user(self, email, firstname, lastname, password=None, role=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstname:
            raise ValueError('Users must have a name')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(
            email=email,
            firstname=firstname,
            lastname=lastname,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, firstname, lastname, password=None):
        user = self.create_user(
            email,
            firstname=firstname,
            lastname=lastname,
            password=password,
            role='administrative'  # Superusers have the 'admin' role
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('medical', 'Medical'),
        ('nursing', 'Nursing'),
        ('allied-health', 'Allied Health'),
        ('support', 'Support'),
        ('management', 'Management'),
        ('administrative', 'Administrative'),
        ('other', 'Other')
        
        
    )

    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='patient')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='useraccount_set',  # Custom related name to avoid clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='useraccount_set',  # Custom related name to avoid clashes
        blank=True,
    )
    def __str__(self):
        return self.email
    


class Patient(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('discharged', 'Discharged'),
        ('observation', 'Observation')
    )
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(db_column='dateofbirth', blank=True, null=True)
    gender = models.CharField(db_column='gender', choices=GENDER_CHOICES, max_length=6)
    contact_number = models.CharField(db_column='contactnumber', unique=True, max_length=20)
    address = models.CharField(db_column='address', max_length=255)
    work = models.CharField(db_column='work', max_length=45, blank=True, null=True)
    height = models.FloatField(db_column='height')
    ssn = models.CharField(db_column='ssn', max_length=255, blank=True, null=True)
    status = models.CharField(db_column='status', choices=STATUS_CHOICES, default='active', max_length=25, blank=True)
    reg_date = models.DateTimeField(default=timezone.now)
    class Meta:
        managed = True
        db_table = 'patients'

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"


class Staff(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    )
    GROUP_CHOICES = (
        ('medical', 'Medical'),
        ('nursing', 'Nursing'),
        ('allied-health', 'Allied Health'),
        ('support', 'Support'),
        ('management', 'Management'),
        ('administrative', 'Administrative'),
        ('other', 'Other')
    )
    WORK_STATUS_CHOICES = (
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('consultant', 'Consultant'),
        ('temporary', 'Temporary')
    )

    AVAILABILITY_CHOICES = (
        ('yes', 'Yes'),
        ('no', 'No')
       
    )
    
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE, related_name='staff_profile')
    avatar = models.ImageField(upload_to='avatars/')
    group = models.CharField(choices=GROUP_CHOICES, max_length=25, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6)
    contact_number = models.CharField(unique=True, max_length=20)
    address = models.CharField(max_length=255)
    work_status = models.CharField(choices=WORK_STATUS_CHOICES, max_length=20)
    specialization = models.CharField(max_length=100)
    assigned_treatment = models.TextField(blank=True)
    working_days = models.JSONField()
    available = models.CharField(choices=AVAILABILITY_CHOICES, default="yes", blank=True, max_length=20)
    appointments = models.ManyToManyField('clinic.Appointment', related_name='appointments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'staff'
        verbose_name = 'Staff Member'
        verbose_name_plural = 'Staff Members'
        indexes = [
            models.Index(fields=['contact_number']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname} - {self.specialization}"
    
