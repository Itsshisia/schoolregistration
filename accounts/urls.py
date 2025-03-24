from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home_view, name='home'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),  # Add logout URL
    path('admin/manage-students/', views.manage_students_view, name='manage_students'),
    path('admin/student/<int:student_id>/', views.student_detail_view, name='student_detail'),  # New URL
    path('admin/send-notification/<int:student_id>/', views.send_notification, name='send_notification'),
    path('admin/generate-admission-report/', views.generate_admission_report, name='generate_admission_report'),
    path('admission-management/', views.admission_management_view, name='admission_management'),
    path('update-admission-status/<int:student_id>/', views.update_admission_status, name='update_admission_status'),
    path('admin/send-notification/<int:student_id>/', views.send_notification, name='send_notification'),
    path('user/admission-management/', views.user_admission_management_view, name='user_admission_management'),
    path('course-enrollment/', views.course_enrollment_view, name='course_enrollment'),
    path('manage-courses/', views.manage_courses_view, name='manage_courses'),
    path('manage-course-approvals/', views.manage_course_approvals, name='manage_course_approvals'),

    path('approval-details/<int:approval_id>/', views.view_approval_details, name='approval_details'),
    path('course-transfer/', views.course_transfer, name='course_transfer'),
    path('course-transfer-status/', views.course_transfer_status, name='course_transfer_status'),
    path('admin/approve-transfer-request/<int:request_id>/', views.approve_transfer_request, name='approve_transfer_request'),
    path('admin/deny-transfer-request/<int:request_id>/', views.deny_transfer_request, name='deny_transfer_request'),
    path('admin/course-transfer-requests/', views.admin_course_transfer_requests, name='admin_course_transfer_requests'),
    path('admin/approve-transfer-request/<int:request_id>/', views.approve_transfer_request, name='approve_transfer_request'),
    path('admin/deny-transfer-request/<int:request_id>/', views.deny_transfer_request, name='deny_transfer_request'),


    path('tickets/submit/', views.submit_ticket, name='submit_ticket'),
    path('admin/tickets/', views.admin_ticket_list, name='admin_ticket_list'),
    path('admin/tickets/<int:ticket_id>/response/', views.admin_ticket_response, name='admin_ticket_response'),
    path('tickets/<int:ticket_id>/responses/', views.get_ticket_responses, name='get_ticket_responses'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),  # ✅ Added this!
    path('tickets/<int:ticket_id>/responses/', views.get_ticket_responses, name='get_ticket_responses'),

    path('book-student-id/', views.book_student_id, name='book_student_id'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment/confirmation/', views.payment_confirmation, name='payment_confirmation'),





    path('course-enrollment/', views.course_enrollment_view, name='course_enrollment'),
    path('make-payment/', views.make_payment_view, name='make_payment'),



    path('fees-payment-details/', views.fees_payment_details, name='fees_payment_details'),
    path('initiate-fees-payment/', views.initiate_fees_payment, name='initiate_fees_payment'),

    path('book-student-id/', views.book_student_id, name='book_student_id'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment-confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('submit-mpesa-code/', views.submit_mpesa_code, name='submit_mpesa_code'),
    path('manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('approve-booking/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('decline-booking/<int:booking_id>/', views.decline_booking, name='decline_booking'),



    path('upload_documents/', views.upload_documents, name='upload_documents'),
    path('download-student-report/', views.download_student_report, name='download_student_report'),
    path('download-registration-slip/<int:approval_id>/', views.download_registration_slip, name='download_registration_slip'),

    path('update_admission_status/<int:student_id>/', views.update_admission_status, name='update_admission_status'),

    path('course-transfer-status/', views.course_transfer_status, name='course_transfer_status'),
    path('ticket/<int:ticket_id>/', views.student_ticket_detail, name='student_ticket_detail'),


    path('admin/approve-transfer-request/<int:request_id>/', views.approve_transfer_request, name='approve_transfer_request'),

    path('enter_verification_code/', views.enter_verification_code, name='enter_verification_code'),
    path('submit_verification_code/', views.submit_verification_code, name='submit_verification_code'),



]



# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # type: ignore





