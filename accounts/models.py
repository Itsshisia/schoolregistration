from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    admission_status = models.CharField(max_length=50, default='Pending')  # Pending, In Review, Verified, Rejected
    profile_completion = models.IntegerField(default=0)

    # Personal Details
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Academic Information
    previous_school = models.CharField(max_length=200, blank=True, null=True)
    high_school_grades = models.CharField(max_length=50, blank=True, null=True)
    entry_program = models.CharField(max_length=100, blank=True, null=True)
    enrollment_year = models.IntegerField(blank=True, null=True)
    program_name = models.CharField(max_length=100, blank=True, null=True)

    # Document Uploads
    id_document = models.FileField(upload_to='documents/', blank=True, null=True)
    transcript = models.FileField(upload_to='documents/', blank=True, null=True)
    admission_letter = models.FileField(upload_to='documents/', blank=True, null=True)
    proof_of_payment = models.FileField(upload_to='documents/', blank=True, null=True)

    # Document Verification Status
    id_document_verified = models.BooleanField(default=False)
    transcript_verified = models.BooleanField(default=False)
    proof_of_payment_verified = models.BooleanField(default=False)

    # Required fields for Django's authentication system
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
        
    notification = models.TextField(blank=True, null=True)

    @property
    def verified_document_count(self):
        count = 0
        if self.id_document_verified:
            count += 1
        if self.transcript_verified:
            count += 1
        if self.proof_of_payment_verified:
            count += 1
        return count
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# Course Model

class Course(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    credits = models.IntegerField()
    semester = models.CharField(max_length=50)
    program_name = models.CharField(max_length=100, null=True, blank=True)  # Make the field nullable
    is_mandatory = models.BooleanField(default=False)
    is_transferable = models.BooleanField(default=True)  # Add this field

    def __str__(self):
        return self.course_name

# Payment Model
class Payment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=50)  # e.g., Tuition, ID Card
    transaction_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.student.username} - {self.payment_type}"

# Course Approval Request Model
class CourseApprovalRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='approval_requests')
    courses = models.ManyToManyField('Course', related_name='approval_requests')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Approval Request by {self.student.username}"

# Approval Status Choices
class ApprovalStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

# Course Approval Model
class CourseApproval(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_approvals')
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING
    )
    feedback = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Approval request by {self.student.username} - {self.status}"
    
    class Meta:
        ordering = ['-submitted_date']
        
# Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    approval = models.ForeignKey(CourseApproval, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.course_code}"
    









class CourseTransferRequest(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transfer_requests')
    from_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='transfer_from')
    to_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='transfer_to')
    reason = models.TextField(default='')
    status = models.CharField(max_length=50, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.from_course.course_code} to {self.to_course.course_code}"
    






    













# models.py
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    ISSUE_TYPES = [
        ('admission', 'Admission'),
        ('fees', 'Fees'),
        ('course', 'Course'),
        ('it', 'IT'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.get_status_display()}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to {self.ticket.subject} by {self.responder.username}"
    














from django.db import models
from django.conf import settings

class StudentIDBooking(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='id_bookings')
    full_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=50, unique=True)
    passport_photo = models.ImageField(upload_to='passport_photos/')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.registration_number}"


class Payment(models.Model):
    booking = models.OneToOneField(
        StudentIDBooking,
        on_delete=models.CASCADE,
        related_name='payment',
        null=True,  # Allow NULL values
        blank=True  # Allow the field to be blank in forms
    )
    mpesa_code = models.CharField(
        max_length=50,
        unique=True,
        null=True,  # Allow NULL values in the database
        blank=True  # Allow the field to be blank in forms
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(
        max_length=15,
        null=True,  # Allow NULL values in the database
        blank=True  # Allow the field to be blank in forms
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.full_name} - {self.mpesa_code}"


class PickupLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    


    # models.py
from django.db import models
from django.conf import settings

class RegistrationSlip(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registration_slips')
    approval = models.ForeignKey('CourseApproval', on_delete=models.CASCADE, related_name='registration_slips')
    generated_date = models.DateTimeField(auto_now_add=True)
    slip_file = models.FileField(upload_to='registration_slips/', blank=True, null=True)

    def __str__(self):
        return f"Registration Slip for {self.student.username} - {self.generated_date}"
    







    # models.py
from django.db import models
from django.conf import settings

class FeesPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fees_payments')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    course_enrolled = models.CharField(max_length=100)
    academic_year = models.CharField(max_length=50)
    tuition_fees = models.DecimalField(max_digits=10, decimal_places=2)
    library_fees = models.DecimalField(max_digits=10, decimal_places=2)
    laboratory_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    hostel_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    examination_fees = models.DecimalField(max_digits=10, decimal_places=2)
    medical_fees = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    payment_status = models.CharField(max_length=20, default='Pending')
    verification_code = models.CharField(max_length=10, blank=True, null=True)  # New field
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} - {self.total_amount}"