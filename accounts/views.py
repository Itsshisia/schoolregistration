from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import User, Course, Enrollment, Payment
'''       # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()'''


from django.shortcuts import render

def home_view(request):
    return render(request, 'accounts/home.html')

from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

def signup_view(request):
    User = get_user_model()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'accounts/signup.html', {"error_message": "Passwords do not match!"})

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {"error_message": "Username already exists! Please choose a different username."})
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html', {"error_message": "Email already exists! Please use a different email."})

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password)  # Creates user with hashed password

        # Redirect user to login page after successful signup
        return redirect('accounts:login')

    # Render the signup form for GET requests
    return render(request, 'accounts/signup.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            # Log the user in
            login(request, user)
            return redirect('accounts:dashboard')
        else:
            # Instead of returning an HttpResponse, pass the error to the template
            return render(request, 'accounts/login.html', {"error_message": "Invalid username or password!"})

    # Render the login form for GET requests
    return render(request, 'accounts/login.html')


def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    student = request.user
    courses = Course.objects.all()
    enrolled_courses = Enrollment.objects.filter(student=student)
    payments = Payment.objects.filter(booking__student=student)

    context = {
        'student': student,
        'courses': courses,
        'enrolled_courses': enrolled_courses,
        'payments': payments,
    }
    return render(request, 'accounts/dashboard.html', context)












from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        # Update personal details
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        user.gender = request.POST.get('gender', user.gender)
        user.nationality = request.POST.get('nationality', user.nationality)
        user.phone_number = request.POST.get('phone_number', user.phone_number)

        # Update academic information
        user.previous_school = request.POST.get('previous_school', user.previous_school)
        user.high_school_grades = request.POST.get('high_school_grades', user.high_school_grades)
        user.entry_program = request.POST.get('entry_program', user.entry_program)
        user.enrollment_year = request.POST.get('enrollment_year', user.enrollment_year)
        user.program_name = request.POST.get('program_name', user.program_name)

        # Handle file uploads
        if 'id_document' in request.FILES:
            user.id_document = request.FILES['id_document']
        if 'transcript' in request.FILES:
            user.transcript = request.FILES['transcript']
        if 'admission_letter' in request.FILES:
            user.admission_letter = request.FILES['admission_letter']

        user.save()
        return redirect('accounts:dashboard')

    context = {
        'student': user,
    }
    return render(request, 'accounts/edit_profile.html', context)









from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user using Django's authentication system
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff and user.is_superuser:
            # Log the user in
            login(request, user)
            return redirect('accounts:admin_dashboard')
        else:
            return HttpResponse("Invalid admin credentials! Please try again.")

    return render(request, 'accounts/adminlogin.html')

def admin_dashboard_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('accounts:admin_login')
    
    # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    # Then use it
    students = User.objects.filter(is_superuser=False)
    courses = Course.objects.all()
    payments = Payment.objects.all()

    context = {
        'students': students,
        'courses': courses,
        'payments': payments,
    }
    return render(request, 'accounts/admindashboard.html', context)


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('accounts:login')










from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensure only admins can access
def manage_students_view(request):
        # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()
    students = User.objects.filter(is_superuser=False)  # Fetch all non-admin users
    context = {
        'students': students,
    }
    return render(request, 'accounts/manage_students.html', context)



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User

@login_required
@user_passes_test(lambda u: u.is_superuser)  # Ensure only admins can access
def student_detail_view(request, student_id):
           # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()
    student = get_object_or_404(User, id=student_id, is_superuser=False)  # Fetch the student
    context = {
        'student': student,
    }
    return render(request, 'accounts/student_detail.html', context)






from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admission_management_view(request):
        # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()

    students = User.objects.filter(is_superuser=False)
    context = {
        'students': students,
    }
    return render(request, 'accounts/admission_management.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_admission_status(request, student_id):
    student = get_object_or_404(User, id=student_id, is_superuser=False)
    if request.method == 'POST':
        new_status = request.POST.get('admission_status')
        student.admission_status = new_status
        student.save()
        return redirect('accounts:admission_management')
    return HttpResponse("Invalid request")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def verify_document(request, student_id, document_type):
    student = get_object_or_404(User, id=student_id, is_superuser=False)
    if document_type == 'id_document':
        student.id_document_verified = True
    elif document_type == 'transcript':
        student.transcript_verified = True
    elif document_type == 'proof_of_payment':
        student.proof_of_payment_verified = True
    student.save()
    return redirect('accounts:admission_management')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def generate_admission_letter(request, student_id):
    student = get_object_or_404(User, id=student_id, is_superuser=False)
    if student.admission_status == 'Verified':
        # Generate admission letter (example: save a dummy file)
        admission_letter_content = f"Admission Letter for {student.first_name} {student.last_name}"
        fs = FileSystemStorage()
        filename = f"admission_letter_{student.id}.txt"
        admission_letter = fs.save(filename, ContentFile(admission_letter_content))
        student.admission_letter = admission_letter
        student.save()
        return redirect('accounts:admission_management')
    return HttpResponse("Admission not verified")





from django.shortcuts import redirect
from django.contrib import messages

@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_notification(request, student_id):
    student = get_object_or_404(User, id=student_id, is_superuser=False)
    if request.method == 'POST':
        notification = request.POST.get('notification')
        student.notification = notification
        student.save()
        messages.success(request, f"Notification sent to {student.username}.")
    return redirect('accounts:admission_management')





from django.http import HttpResponse
import csv





@login_required
def user_admission_management_view(request):
    student = request.user  # Get the logged-in student
    if request.method == 'POST':
        # Handle file uploads
        if 'id_document' in request.FILES:
            student.id_document = request.FILES['id_document']
        if 'transcript' in request.FILES:
            student.transcript = request.FILES['transcript']
        if 'proof_of_payment' in request.FILES:
            student.proof_of_payment = request.FILES['proof_of_payment']
        student.save()
        return redirect('accounts:user_admission_management')

    context = {
        'student': student,
    }
    return render(request, 'accounts/user_admission_management.html', context)








from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CourseApprovalRequest

@login_required
def manage_courses_view(request):
    # Fetch all approval requests
    approval_requests = CourseApprovalRequest.objects.all()
    context = {
        'approval_requests': approval_requests,
    }
    return render(request, 'accounts/manage_courses.html', context)



# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Course, Enrollment, CourseApproval





@login_required
def manage_course_approvals(request):
    # Check if user is staff/admin
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    
    approvals = CourseApproval.objects.filter(status='pending')
    
    if request.method == 'POST':
        approval_id = request.POST.get('approval_id')
        action = request.POST.get('action')
        feedback = request.POST.get('feedback', '')
        
        approval = CourseApproval.objects.get(id=approval_id)
        
        if action == 'approve':
            approval.status = 'approved'
            approval.feedback = feedback
            approval.save()
            messages.success(request, f'Approval request by {approval.student.username} has been approved.')
        
        elif action == 'reject':
            approval.status = 'rejected'
            approval.feedback = feedback
            approval.save()
            messages.success(request, f'Approval request by {approval.student.username} has been rejected.')
    
    context = {
        'pending_approvals': approvals,
    }
    return render(request, 'accounts/manage_course_approvals.html', context)

@login_required
def view_approval_details(request, approval_id):
    # Check if user is staff/admin or the student who submitted the approval
    approval = CourseApproval.objects.get(id=approval_id)
    
    if not (request.user.is_staff or request.user == approval.student):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:dashboard')
    
    enrollments = Enrollment.objects.filter(approval=approval)
    total_credits = enrollments.aggregate(total=Sum('course__credits'))['total'] or 0
    
    context = {
        'approval': approval,
        'enrollments': enrollments,
        'total_credits': total_credits,
    }
    return render(request, 'accounts/approval_details.html', context)



















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, CourseTransferRequest

@login_required
def course_transfer(request):
    if request.method == 'POST':
        from_course_id = request.POST.get('from_course')
        to_course_id = request.POST.get('to_course')
        reason = request.POST.get('reason')

        try:
            from_course = get_object_or_404(Course, id=from_course_id)
            to_course = get_object_or_404(Course, id=to_course_id)

            CourseTransferRequest.objects.create(
                student=request.user,
                from_course=from_course,
                to_course=to_course,
                reason=reason
            )
            return redirect('course_transfer_status')
        except Exception as e:
            return render(request, 'accounts/course_transfer.html', {
                'current_courses': request.user.enrollments.all(),
                'transferable_courses': Course.objects.filter(is_transferable=True),
            })

    current_courses = request.user.enrollments.all()
    transferable_courses = Course.objects.filter(is_transferable=True)
    return render(request, 'accounts/course_transfer.html', {
        'current_courses': current_courses,
        'transferable_courses': transferable_courses,
    })


from django.contrib.auth.decorators import login_required
from .models import CourseTransferRequest

@login_required
def course_transfer_status(request):
    transfer_requests = CourseTransferRequest.objects.filter(student=request.user)
    return render(request, 'accounts/course_transfer_status.html', {
        'transfer_requests': transfer_requests,
    })



def admin_course_transfer_requests(request):
    transfer_requests = CourseTransferRequest.objects.filter(status='Pending')
    return render(request, 'accounts/admin_course_transfer_requests.html', {
        'transfer_requests': transfer_requests,
    })


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import CourseTransferRequest

def approve_transfer_request(request, request_id):
    transfer_request = get_object_or_404(CourseTransferRequest, id=request_id)
    transfer_request.status = 'Approved'
    transfer_request.save()

    # Notify the admin
    messages.success(request, f"Course transfer request for {transfer_request.student.username} has been approved.")

    # Redirect to the admin course transfer requests page
    return redirect('accounts:admin_course_transfer_requests')

def deny_transfer_request(request, request_id):
    transfer_request = get_object_or_404(CourseTransferRequest, id=request_id)
    transfer_request.status = 'Rejected'
    transfer_request.save()

    # Notify the admin
    messages.error(request, f"Course transfer request for {transfer_request.student.username} has been denied.")

    # Redirect to the admin course transfer requests page
    return redirect('accounts:admin_course_transfer_requests')














# views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Ticket, TicketResponse


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Ticket, TicketResponse

@login_required
def submit_ticket(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        ticket = Ticket.objects.create(
            student=request.user,
            subject=subject,
            issue_type=issue_type,
            description=description
        )
        return JsonResponse({"message": "Ticket submitted successfully!", "ticket_id": ticket.id})

    # ✅ Get the latest ticket to ensure "View Responses" button visibility
    latest_ticket = Ticket.objects.filter(student=request.user).order_by('-created_at').first()
    return render(request, 'accounts/submit_ticket.html', {'latest_ticket': latest_ticket})


@login_required
def get_ticket_responses(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    responses = list(ticket.responses.values("responder__username", "message", "timestamp"))
    return JsonResponse({"responses": responses})








@login_required
def admin_ticket_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    if request.method == "POST":
        message = request.POST.get('message')
        feedback = request.POST.get('feedback', '')  # Add feedback field
        
        # Create a response
        response = TicketResponse.objects.create(
            ticket=ticket,
            responder=request.user,
            message=message
        )

        # Update ticket status and feedback
        ticket.status = 'in_progress' if ticket.status == 'open' else 'resolved'
        ticket.feedback = feedback  # Save feedback
        ticket.save()

        return JsonResponse({"message": "Response added successfully!"})

    return render(request, 'accounts/admin_ticket_response.html', {'ticket': ticket})


@login_required
def admin_ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')
    return render(request, 'accounts/admin_ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'accounts/ticket_detail.html', {'ticket': ticket})



@login_required
def student_ticket_detail(request, ticket_id):
    # Ensure the ticket belongs to the logged-in student
    ticket = get_object_or_404(Ticket, id=ticket_id, student=request.user)
    
    # Fetch all responses for the ticket
    responses = TicketResponse.objects.filter(ticket=ticket).order_by('timestamp')
    
    return render(request, 'accounts/student_ticket_detail.html', {
        'ticket': ticket,
        'responses': responses,
    })
















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentIDBooking, Payment, PickupLocation
import requests
from django.conf import settings

@login_required
def book_student_id(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        registration_number = request.POST.get('registration_number')
        passport_photo = request.FILES.get('passport_photo')
        
        # Check if registration number already exists
        if StudentIDBooking.objects.filter(registration_number=registration_number).exists():
            messages.error(request, 'This registration number is already in use. Please verify your registration number.')
            return render(request, 'accounts/book_student_id.html')
        
        booking = StudentIDBooking(
            student=request.user,
            full_name=full_name,
            registration_number=registration_number,
            passport_photo=passport_photo
        )
        booking.save()
        messages.success(request, 'Student ID booking submitted successfully! Proceed to payment.')
        return redirect('accounts:payment', booking_id=booking.id)
    
    return render(request, 'accounts/book_student_id.html')


@login_required
def payment(request, booking_id):
    booking = get_object_or_404(StudentIDBooking, id=booking_id, student=request.user)
    
    # Check if a payment already exists for this booking
    if Payment.objects.filter(booking=booking).exists():
        messages.warning(request, 'A payment for this booking already exists.')
        return redirect('accounts:payment_confirmation')
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = 100  # Fixed amount for ID booking
        
        # Initiate M-Pesa STK Push
        response = initiate_stk_push(phone_number, amount, booking.id)
        if response.get('ResponseCode') == '0':
            Payment.objects.create(
                booking=booking,
                phone_number=phone_number,
                amount=amount,
                mpesa_code=response.get('CheckoutRequestID')
            )
            messages.success(request, 'Payment initiated successfully. Check your phone for the M-Pesa prompt.')
            return redirect('accounts:payment_confirmation')
        else:
            messages.error(request, 'Failed to initiate payment. Please try again.')
    
    return render(request, 'accounts/payment.html', {'booking': booking})


@login_required
def payment_confirmation(request):
    return render(request, 'accounts/payment_confirmation.html')


def manage_bookings(request):
    bookings = StudentIDBooking.objects.all()
    return render(request, 'accounts/manage_bookings.html', {'bookings': bookings})


import requests
import base64
from datetime import datetime
from django.conf import settings

# Base64 encoding function
def __base64encode(data):
    return base64.b64encode(data.encode("ascii")).decode("ascii")

# Generate M-Pesa token
def generate_mpesa_token(consumer_key, consumer_secret):
    password = __base64encode(f"{consumer_key}:{consumer_secret}")
    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers={'Authorization': f'Basic {password}'}
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to generate M-Pesa token")

# Initiate STK Push
def initiate_stk_push(phone_number, amount, booking_id):
    try:
        # M-Pesa credentials
        consumer_key = "zKRjXuvclUiGyIXD35NjPQq9hQxbrkdP"
        consumer_secret = "UwUxLeTKzdJ4GbiN"
        lipa_na_mpesa_online_passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        lipa_na_mpesa_online_shortcode = "174379"

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

        # Generate password
        password = __base64encode(f"{lipa_na_mpesa_online_shortcode}{lipa_na_mpesa_online_passkey}{timestamp}")

        # Generate M-Pesa token
        access_token = generate_mpesa_token(consumer_key, consumer_secret)

        # Prepare payload
        payload = {
            "BusinessShortCode": lipa_na_mpesa_online_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": lipa_na_mpesa_online_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": f"{settings.BASE_URL}/mpesa-callback/",
            "AccountReference": f"Student-ID-Booking-{booking_id}",
            "TransactionDesc": "Student ID Booking Payment",
        }

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Send STK Push request
        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers,
        )

        # Log the response for debugging
        print("STK Push Response:", response.text)
        print("Payload:", payload)
        print("Headers:", headers)

        # Handle the response
        if response.status_code == 200:
            payment_data = response.json()
            return payment_data
        else:
            raise Exception(f"STK Push failed with status code {response.status_code}: {response.text}")

    except Exception as e:
        print(f"Error initiating STK Push: {str(e)}")
        raise







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentIDBooking, Payment

@login_required
def submit_mpesa_code(request):
    if request.method == 'POST':
        mpesa_code = request.POST.get('mpesa_code')
        booking = StudentIDBooking.objects.filter(student=request.user).first()
        
        if booking:
            # Save the M-Pesa code to the Payment model
            payment, created = Payment.objects.get_or_create(booking=booking)
            payment.mpesa_code = mpesa_code
            payment.save()
            
            messages.success(request, 'M-Pesa code submitted successfully. Admin will verify your payment.')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'No booking found for this user.')
            return redirect('accounts:payment_confirmation')
    
    messages.error(request, 'Invalid request.')
    return redirect('accounts:payment_confirmation')

@login_required
def approve_booking(request, booking_id):
    booking = get_object_or_404(StudentIDBooking, id=booking_id)
    booking.is_paid = True
    booking.save()
    messages.success(request, 'Booking approved successfully!')
    return redirect('accounts:manage_bookings')

@login_required
def decline_booking(request, booking_id):
    booking = get_object_or_404(StudentIDBooking, id=booking_id)
    booking.is_paid = False
    booking.save()
    messages.success(request, 'Booking declined successfully!')
    return redirect('accounts:manage_bookings')














from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import csv

def user_admission_management(request):
    user = get_object_or_404(User, user=request.user)
    context = {
        'user': user,
        'admission_status': user.admission_status,
        'id_document': user.id_document,
        'transcript': user.transcript,
        'proof_of_payment': user.proof_of_payment,
    }
    return render(request, 'accounts/user_admission_management.html', context)

@csrf_exempt
def upload_documents(request):
    if request.method == 'POST':
        user = get_object_or_404(User, user=request.user)
        id_document = request.FILES.get('id_document')
        transcript = request.FILES.get('transcript')
        proof_of_payment = request.FILES.get('proof_of_payment')

        if id_document:
            user.id_document = id_document
        if transcript:
            user.transcript = transcript
        if proof_of_payment:
            user.proof_of_payment = proof_of_payment

        user.save()
        return JsonResponse({'status': 'success', 'message': 'Documents uploaded successfully!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def admin_admission_management(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/admin_admission_management.html', context)

@csrf_exempt
def update_admission_status(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        new_status = request.POST.get('admission_status')
        if new_status in ['Pending', 'In Review', 'Verified', 'Rejected']:
            user.admission_status = new_status
            user.save()
            return JsonResponse({'status': 'success', 'message': f'Status updated to {new_status}.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid status.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def fetch_admission_status(request):
    user = get_object_or_404(User, user=request.user)
    return JsonResponse({'status': user.admission_status})

def generate_admission_report(request):
    users = User.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="admission_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Username', 'Admission Status', 'ID Document', 'Transcript', 'Proof of Payment'])
    for user in users:
        writer.writerow([
            user.username,
            user.admission_status,
            user.id_document.url if user.id_document else 'Not Uploaded',
            user.transcript.url if user.transcript else 'Not Uploaded',
            user.proof_of_payment.url if user.proof_of_payment else 'Not Uploaded',
        ])
    return response






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Course, Enrollment, CourseApproval
from django.contrib import messages
import requests
import base64
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, CourseApproval

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, CourseApproval

def course_enrollment_view(request):
    student = request.user  # Get the logged-in student

    # Fetch all elective courses (no program_name filter)
    elective_courses = Course.objects.filter(is_mandatory=False)

    # Debug: Print elective courses
    print("Elective Courses:", elective_courses)

    # Calculate total credit hours for enrolled courses (if any)
    enrolled_courses = Enrollment.objects.filter(student=student)
    total_credit_hours = enrolled_courses.aggregate(total_credits=Sum('course__credits'))['total_credits'] or 0

    # Get latest approval status if any
    latest_approval = CourseApproval.objects.filter(student=student).first()

    if request.method == 'POST':
        if 'elective_courses' in request.POST:
            # Handle elective course selection
            selected_electives = request.POST.getlist('elective_courses')
            if not selected_electives:
                messages.error(request, 'Please select at least one elective course.')
                return redirect('accounts:course_enrollment')
            
            for course_id in selected_electives:
                try:
                    course_id = int(course_id)  # Convert to integer
                    course = Course.objects.get(id=course_id)
                    Enrollment.objects.get_or_create(student=student, course=course)
                except (ValueError, Course.DoesNotExist):
                    messages.error(request, f'Invalid course ID: {course_id}')
                    return redirect('accounts:course_enrollment')
            
            messages.success(request, 'Elective courses have been selected successfully.')
            return redirect('accounts:course_enrollment')
        
        elif 'submit_approval' in request.POST:
            # Check if student has any courses enrolled
            if not enrolled_courses.exists():
                messages.error(request, 'You need to select at least one course before submitting for approval.')
                return redirect('accounts:course_enrollment')
            
            # Create approval request
            approval = CourseApproval.objects.create(
                student=student,
                status='pending'
            )
            
            # Link all enrollments to this approval
            enrolled_courses.update(approval=approval)
            
            messages.success(request, 'Your course selection has been submitted for approval.')
            return redirect('accounts:course_enrollment')

    context = {
        'mandatory_courses': Course.objects.filter(is_mandatory=True),  # Optional: Show mandatory courses if needed
        'elective_courses': elective_courses,
        'total_credit_hours': total_credit_hours,
        'enrolled_courses': enrolled_courses,
        'latest_approval': latest_approval,
    }
    return render(request, 'accounts/course_enrollment.html', context)
@login_required
def make_payment_view(request):
    return render(request, 'accounts/make_payment.html')















from django.http import HttpResponse
import csv
from django.shortcuts import get_list_or_404
from .models import User  # Use your custom User model

def download_student_report(request):

           # Import User model first
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Fetch all users (students)
    students = get_list_or_404(User)

    # Create the HttpResponse object with CSV headers
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_report.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Username', 'First Name', 'Last Name', 'Email', 'Admission Status', 'Profile Completion'])

    # Write student data to the CSV
    for student in students:
        writer.writerow([
            student.username,
            student.first_name,
            student.last_name,
            student.email,
            student.admission_status,
            student.profile_completion,
        ])

    return response










# views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate
from io import BytesIO
from .models import CourseApproval

def download_registration_slip(request, approval_id):
    try:
        # Fetch the approval object
        approval = get_object_or_404(CourseApproval, id=approval_id)
        student = request.user  # Get the logged-in student
        enrolled_courses = approval.enrollments.filter(student=student)  # Filter enrolled courses for the student

        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Create the PDF object using SimpleDocTemplate for better layout control
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            name="TitleStyle",
            parent=styles["Title"],
            fontSize=24,
            textColor=colors.darkblue,
            spaceAfter=20,
            alignment=1,  # Center alignment
        )
        heading_style = ParagraphStyle(
            name="HeadingStyle",
            parent=styles["Heading2"],
            fontSize=16,
            textColor=colors.darkgreen,
            spaceAfter=10,
        )
        body_style = ParagraphStyle(
            name="BodyStyle",
            parent=styles["BodyText"],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=10,
        )

        # Content to be added to the PDF
        content = []

        # Add a captivating welcome message
        welcome_message = """
        <b>Welcome to Your Course Enrollment Summary!</b><br/><br/>
        Congratulations on taking this important step in your academic journey. 
        Your dedication and hard work will pave the way for a bright future. 
        Keep striving for excellence!
        """
        content.append(Paragraph(welcome_message, body_style))
        content.append(Spacer(1, 20))  # Add space

        # Add a motivational quote
        motivational_quote = """
        <i>"The future belongs to those who believe in the beauty of their dreams."</i> - Eleanor Roosevelt
        """
        content.append(Paragraph(motivational_quote, body_style))
        content.append(Spacer(1, 20))  # Add space

        # Add the title
        content.append(Paragraph("Course Enrollment Registration Slip", title_style))
        content.append(Spacer(1, 20))  # Add space

        # Add student details
        student_details = f"""
        <b>Student Username:</b> {student.username}<br/>
        <b>Student Email:</b> {student.email}<br/>
        <b>Approval Status:</b> {approval.status.capitalize()}<br/>
        <b>Approval Date:</b> {approval.submitted_date.strftime('%Y-%m-%d')}<br/>
        """
        content.append(Paragraph(student_details, body_style))
        content.append(Spacer(1, 20))  # Add space

        # Add enrolled courses as a table
        course_data = [["Course Code", "Course Name", "Credits"]]
        for enrollment in enrolled_courses:
            course_data.append([
                enrollment.course.course_code,
                enrollment.course.course_name,
                str(enrollment.course.credits),
            ])

        course_table = Table(course_data)
        course_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),  # Header background
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Header font
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Header padding
            ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),  # Table body background
            ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Grid lines
        ]))

        content.append(course_table)

        # Build the PDF content
        pdf.build(content)

        # File response with the PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="registration_slip_{student.username}.pdf"'
        return response

    except Exception as e:
        # Log the error for debugging
        print(f"Error generating PDF: {e}")
        # Return an error message to the user
        return HttpResponse("Something went wrong. Please try again later or contact your organization.", status=500)
    








from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FeesPayment
import requests
import base64
from datetime import datetime
import re

# M-Pesa credentials
CONSUMER_KEY = "zKRjXuvclUiGyIXD35NjPQq9hQxbrkdP"
CONSUMER_SECRET = "UwUxLeTKzdJ4GbiN"
LIPA_NA_MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
LIPA_NA_MPESA_SHORTCODE = "174379"
MPESA_CALLBACK_URL = "https://www.nurubay.com/mpesa-callback/"

@login_required
def fees_payment_details(request):
    enrollment = Enrollment.objects.filter(student=request.user).first()

    """Display student details and fee breakdown."""
    student = request.user
    context = {
        'username': student.username,
        'email': student.email,
        #'course_enrolled': "Computer Science",  # Replace with dynamic logic
        'course_enrolled': enrollment.course.course_name if enrollment else "Not Enrolled",
        'academic_year': "2024/2025",  # Replace with dynamic logic
        'tuition_fees': 50000.00,
        'library_fees': 5000.00,
        'laboratory_fees': 3000.00,
        'hostel_fees': 20000.00,
        'examination_fees': 2000.00,
        'medical_fees': 1500.00,
        'other_charges': 1000.00,
        'total_amount': 50000.00 + 5000.00 + 3000.00 + 20000.00 + 2000.00 + 1500.00 + 1000.00,
    }
    return render(request, 'accounts/fees_payment_details.html', context)

@login_required
def initiate_fees_payment(request):
    """Handle the STK push logic."""
    if request.method == 'POST':
        # Fetch student details
        student = request.user
        phone_number = request.POST.get('phone_number')

        # Validate phone number
        phone_number = re.sub(r"^0", "254", phone_number) if phone_number.startswith(('01', '07')) else phone_number

        # Fee breakdown (same as in fees_payment_details)
        total_amount = 50000.00 + 5000.00 + 3000.00 + 20000.00 + 2000.00 + 1500.00 + 1000.00

        # Create a FeesPayment record
        payment = FeesPayment.objects.create(
            user=student,
            #username=student.username,
            email=student.email,
            course_enrolled="Computer Science",  # Replace with dynamic logic
            academic_year="2023/2024",  # Replace with dynamic logic
            tuition_fees=50000.00,
            library_fees=5000.00,
            laboratory_fees=3000.00,
            hostel_fees=20000.00,
            examination_fees=2000.00,
            medical_fees=1500.00,
            other_charges=1000.00,
            total_amount=total_amount,
            phone_number=phone_number,
            payment_status='Pending'
        )

        # Generate M-Pesa payment request
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((LIPA_NA_MPESA_SHORTCODE + LIPA_NA_MPESA_PASSKEY + timestamp).encode()).decode()

        payload = {
            "BusinessShortCode": LIPA_NA_MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": total_amount,
            "PartyA": phone_number,
            "PartyB": LIPA_NA_MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": MPESA_CALLBACK_URL,
            "AccountReference": f"FeesPayment-{payment.id}",
            "TransactionDesc": "Fees Payment"
        }

        headers = {
            "Authorization": f"Bearer {generete_mpesa_token()}",
            "Content-Type": "application/json"
        }

        # Send the payment request to M-Pesa
        response = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            payment.transaction_id = response.json().get('CheckoutRequestID')
            payment.save()
            return JsonResponse({"status": "success", "message": "Payment initiated. Please check your phone to complete the payment."})
        else:
            payment.payment_status = 'Failed'
            payment.save()
            return JsonResponse({"status": "error", "message": "Failed to initiate payment. Please try again."})

    return render(request, 'accounts/initiate_fees_payment.html')

def generete_mpesa_token():
    """Generate M-Pesa access token."""
    auth = base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers={'Authorization': f'Basic {auth}'}
    )
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa callback."""
    if request.method == 'POST':
        data = request.json()
        transaction_id = data.get('CheckoutRequestID')
        result_code = data.get('ResultCode')

        if result_code == 0:
            # Payment was successful
            payment = FeesPayment.objects.get(transaction_id=transaction_id)
            payment.payment_status = 'Completed'
            payment.save()
        else:
            # Payment failed
            payment = FeesPayment.objects.get(transaction_id=transaction_id)
            payment.payment_status = 'Failed'
            payment.save()

        return HttpResponse(status=200)
    return HttpResponse(status=400)





from django.shortcuts import render, get_object_or_404
from .models import CourseApproval, Enrollment  # Replace with your actual models

def approval_details(request, approval_id):
    # Fetch the course approval details
    approval = get_object_or_404(CourseApproval, id=approval_id)
    
    # Fetch the current enrolled courses for the student
    enrolled_courses = Enrollment.objects.filter(student=approval.student, status='enrolled')
    
    # Render the details in a template
    return render(request, 'accounts/approval_details.html', {
        'approval': approval,
        'enrolled_courses': enrolled_courses  # Pass enrolled courses to the template
    })




from django.shortcuts import render

def course_transfer_status(request):
    # Your logic here
    return render(request, 'accounts/course_transfer_status.html')














from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FeesPayment

@login_required
def enter_verification_code(request):
    """Render the template for entering the verification code."""
    return render(request, 'accounts/enter_verification_code.html')

@login_required
def submit_verification_code(request):
    """Handle the submission of the verification code."""
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        
        # Fetch the latest payment for the user
        payment = FeesPayment.objects.filter(user=request.user).last()
        
        if payment:
            # Update the payment with the verification code
            payment.verification_code = verification_code
            payment.save()
            return JsonResponse({"status": "success", "message": "Verification code submitted successfully."})
        else:
            return JsonResponse({"status": "error", "message": "No payment found."})
    
    return JsonResponse({"status": "error", "message": "Invalid request method."})