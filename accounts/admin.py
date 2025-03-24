from django.contrib import admin
from .models import (
    User, Course, Payment, CourseApprovalRequest, CourseApproval, Enrollment,
    CourseTransferRequest, Ticket, TicketResponse, StudentIDBooking, PickupLocation,
    RegistrationSlip, FeesPayment
)

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'student_id', 'admission_status', 'profile_completion')
    search_fields = ('username', 'email', 'student_id')
    list_filter = ('admission_status', 'is_staff', 'is_superuser')
    readonly_fields = ('verified_document_count',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'semester', 'program_name', 'is_mandatory', 'is_transferable')
    search_fields = ('course_code', 'course_name')
    list_filter = ('semester', 'program_name', 'is_mandatory', 'is_transferable')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'mpesa_code', 'amount', 'phone_number', 'payment_status', 'created_at')
    search_fields = ('booking__full_name', 'mpesa_code', 'phone_number')
    list_filter = ('payment_status', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(CourseApprovalRequest)
class CourseApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'submitted_at', 'is_approved')
    search_fields = ('student__username',)
    list_filter = ('is_approved', 'submitted_at')

@admin.register(CourseApproval)
class CourseApprovalAdmin(admin.ModelAdmin):
    list_display = ('student', 'submitted_date', 'status', 'feedback')
    search_fields = ('student__username',)
    list_filter = ('status', 'submitted_date')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'approval')
    search_fields = ('student__username', 'course__course_code')
    list_filter = ('enrollment_date', 'course__course_code')

@admin.register(CourseTransferRequest)
class CourseTransferRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'from_course', 'to_course', 'reason', 'status', 'created_at')
    search_fields = ('student__username', 'from_course__course_code', 'to_course__course_code')
    list_filter = ('status', 'created_at')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'issue_type', 'status', 'created_at')
    search_fields = ('student__username', 'subject')
    list_filter = ('issue_type', 'status', 'created_at')

@admin.register(TicketResponse)
class TicketResponseAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'responder', 'timestamp')
    search_fields = ('ticket__subject', 'responder__username')
    list_filter = ('timestamp',)

@admin.register(StudentIDBooking)
class StudentIDBookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'full_name', 'registration_number', 'is_paid', 'created_at')
    search_fields = ('student__username', 'registration_number')
    list_filter = ('is_paid', 'created_at')

@admin.register(PickupLocation)
class PickupLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')

@admin.register(RegistrationSlip)
class RegistrationSlipAdmin(admin.ModelAdmin):
    list_display = ('student', 'approval', 'generated_date')
    search_fields = ('student__username', 'approval__student__username')
    list_filter = ('generated_date',)

@admin.register(FeesPayment)
class FeesPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'course_enrolled', 'academic_year', 'total_amount', 'payment_status', 'verification_code', 'created_at')
    search_fields = ('user__username', 'full_name', 'course_enrolled')
    list_filter = ('payment_status', 'created_at')