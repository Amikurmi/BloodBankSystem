from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .models import UserProfile, DonorProfile, RecipientProfile, BloodDonation, BloodRequest, BloodBank, DonationCamp, DonorRegistration
from django.views.generic import ListView
from .forms import DonationCampForm, RegistrationForm, BloodDonationForm,BloodBankForm
import logging
from urllib.parse import urlencode
from django.db import IntegrityError
from django.utils.timezone import localtime
from django.utils.timezone import make_aware
from datetime import datetime, time, date, timedelta
from datetime import datetime, timedelta
from django.urls import reverse
from .forms import DonorProfileForm, RecipientProfileForm
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import UserProfile
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str



def is_not_admin(user):
    return not user.is_superuser

logger = logging.getLogger(__name__)

def send_email(subject, message, from_email, to_email_list):
    try:
        send_mail(subject, message, from_email, to_email_list, fail_silently=False)
        logger.info(f"Email sent to {to_email_list}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email_list}: {e}")

def index(request):
    return render(request, 'index.html')



# def register(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user_type = request.POST.get('user_type')

#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists. Please choose a different username.")
#         else:
#             if len(password) < 8:
#                 messages.error(request, "Password must be at least 8 characters long.")
#                 return redirect('register')

#             user = User.objects.create_user(username=username, email=email, password=password)
#             user.is_active = False  # User must activate their account via email
#             user.save()

#             user_profile = UserProfile(user=user, user_type=user_type)
#             user_profile.save()

#             # Generate activation token and URL
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

#             # Prepare email content
#             subject = 'Activate your account'
#             message = render_to_string('register/activation_email.html', {
#                 'username': username,
#                 'activation_link': activation_link,
#             })

#             # Send activation email
#             email = EmailMessage(
#                 subject,
#                 message,
#                 'amitkurmiq18@gmail.com',
#                 [email],
#             )
#             email.content_subtype = "html"  # Main content is now text/html
#             email.send()

#             # Redirect to activation page
#             context = {
#                 'email': email
#             }
#             return render(request, 'register/activation_page.html', context)

#     return render(request, 'register/register.html')


# def activate(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, "Thank you for your email confirmation.")
#         return redirect('donor_profile')
#     else:
#         messages.error(request, "Activation link is invalid!")
#         return redirect('register')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         # Debugging: Log the username and password entered
#         print(f"Attempting login with Username: {username}, Password: {password}")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, "Login successful!")
#             return redirect('home')
#         else:
#             messages.error(request, "Failed login attempt. Username or password is incorrect.")
    
#     return render(request, 'register/login.html')
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            user_profile = UserProfile(user=user, user_type=user_type)
            user_profile.save()
            messages.success(request, "User created successfully.")

            if user_type == 'donor':
                return redirect('donor_profile', user_profile_id=user_profile.id)
            elif user_type == 'recipient':
                return redirect('recipient_profile', user_profile_id=user_profile.id)
            else:
                messages.error(request, "Invalid user type selected.")

    return render(request, 'register/register.html')

def donor_profile(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        contact_number = request.POST.get('contact_number')
        
        DonorProfile.objects.create(
            user=user_profile,
            first_name=first_name,
            last_name=last_name,
            age=age,
            contact_number=contact_number
        )
        messages.success(request, "Donor profile created successfully.")
        return redirect('login')
    
    return render(request, 'donor/donor_profile.html', {'user_profile': user_profile})

def recipient_profile(request, user_profile_id):
    user_profile = UserProfile.objects.get(id=user_profile_id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        
        RecipientProfile.objects.create(
            user=user_profile,
            first_name=first_name,
            last_name=last_name,
            age=age,
            contact_number=contact_number,
            address=address
        )
        messages.success(request, "Recipient profile created successfully.")
        return redirect('login')
    
    return render(request, 'recipient/recipient_profile.html', {'user_profile': user_profile})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in successfully.")
            
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.user_type == 'admin':
                return redirect('admin_dashboard')  # Redirect admin to a special dashboard
            elif user_profile.user_type == 'donor':
                return redirect('index')
            elif user_profile.user_type == 'recipient':
                return redirect('index')
            else:
                return redirect('index')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
                logger.warning(f"Failed login attempt for username: {username} due to incorrect password.")
            else:
                messages.error(request, 'Username not found. Please enter a correct username.')
                logger.warning(f"Failed login attempt for username: {username} due to non-existent username.")
            return render(request, 'register/login.html')
    
    return render(request, 'register/login.html')

@login_required(login_url='/login')
def home(request):
    user_profile = request.user.userprofile
    
    # Redirect based on user type
    if user_profile.user_type == 'donor':
        return redirect('donor_dashboard')
    elif user_profile.user_type == 'recipient':
        return redirect('recipient_dashboard')
    else:
        return redirect('index')  # In case the user type doesn't match

@login_required(login_url='/login')
def donor_dashboard(request):
    if request.user.userprofile.user_type != 'donor':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')
    
    try:
        donor_profile = DonorProfile.objects.get(user=request.user.userprofile)
    except DonorProfile.DoesNotExist:
        messages.error(request, "Donor profile does not exist. Please complete your profile.")
        return redirect('donor_profile', user_profile_id=request.user.userprofile.id)
    
    return render(request, 'donor/dashboard.html', {'donor_profile': donor_profile})

@login_required(login_url='/login')
def recipient_dashboard(request):
    if request.user.userprofile.user_type != 'recipient':
        messages.error(request, "You do not have access to this page.")
        return redirect('home')
    
    try:
        recipient_profile = RecipientProfile.objects.get(user=request.user.userprofile)
    except RecipientProfile.DoesNotExist:
        messages.error(request, "Recipient profile does not exist. Please complete your profile.")
        return redirect('recipient_profile', user_profile_id=request.user.userprofile.id)
    
    return render(request, 'recipient/dashboard.html', {'recipient_profile': recipient_profile})

@staff_member_required
def admin_dashboard(request):
    # Fetch data to display on the dashboard
    messages.error(request, "You are logged in as an admin, and you cannot perform this action.")
    blood_banks_count = BloodBank.objects.count()
    donations_count = BloodDonation.objects.count()
    camps_count = DonationCamp.objects.count()
    requests_count = BloodRequest.objects.count()
    donors_count = DonorProfile.objects.count()
    recipients_count = RecipientProfile.objects.count()

    context = {
        'blood_banks_count': blood_banks_count,
        'donations_count': donations_count,
        'camps_count': camps_count,
        'requests_count': requests_count,
        'donors_count': donors_count,
        'recipients_count': recipients_count,
    }

    return render(request, 'admin/dashboard.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('email')

        send_email(subject, message, from_email, ['amitkurmiq18@gmail.com'])
        return redirect('contact_success')

    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')


# @login_required
# def donate_blood(request):
#     try:
#         user_profile = request.user.userprofile
#         donor_profile = DonorProfile.objects.get(user=user_profile)

#         if request.method == 'POST':
#             form = BloodDonationForm(request.POST)
#             if form.is_valid():
#                 blood_donation = form.save(commit=False)
#                 blood_donation.donor = donor_profile
#                 blood_donation.donation_date = timezone.now()  # You can set this to any date/time if needed
#                 blood_donation.save()
#                 return redirect('donation_success')  # Redirect to a success page or some other page
#         else:
#             form = BloodDonationForm()

#         return render(request, 'donor/donate_blood.html', {'form': form, 'donor_profile': donor_profile})

#     except DonorProfile.DoesNotExist:
#         return redirect('register')
    

# def donation_success(request):
#     return render(request, 'donor/donation_success.html')

# @user_passes_test(is_not_admin, login_url='admin_dashboard')
# @login_required(login_url='/login')
# def donate_blood(request, camp_id):
#     user_profile = get_object_or_404(UserProfile, user=request.user)

#     if user_profile.user_type == 'admin':
#         messages.error(request, 'Admins cannot donate blood.')
#         return redirect('home')

#     if user_profile.user_type == 'recipient':
#         query_params = urlencode({
#             'message': 'You are logged in as a recipient, so you cannot donate blood.',
#             'link_text': 'Go to Request Blood',
#             'link_url': '/request_blood'
#         })
#         return HttpResponseRedirect(f'/message/?{query_params}')

#     try:
#         donor_profile = DonorProfile.objects.get(user=user_profile)
#     except DonorProfile.DoesNotExist:
#         messages.error(request, "You need to complete your donor profile first.")
#         return redirect('donor_profile', user_profile_id=user_profile.id)

#     if donor_profile.age < 18 or donor_profile.age > 55:
#         messages.error(request, "You must be between 18 and 55 years old to donate blood.")
#         return redirect('donation_status')

#     camp = get_object_or_404(DonationCamp, id=camp_id, date__gte=timezone.now())

#     three_months_ago = timezone.now() - timedelta(days=90)
#     last_donation = BloodDonation.objects.filter(user=donor_profile, donation_date__gte=three_months_ago).first()
#     if last_donation:
#         messages.error(request, "You cannot donate blood more than once in a 3-month period.")
#         return redirect('donation_status')

#     if request.method == 'POST':
#         form = BloodDonationForm(request.POST)
#         if form.is_valid():
#             blood_donation = form.save(commit=False)
#             blood_donation.user = donor_profile
#             blood_donation.camp = camp  # Associate donation with the specific camp
#             blood_donation.donation_date = camp.date  # Set the donation date to the camp date
#             try:
#                 blood_donation.save()
#                 messages.success(request, "Donation recorded successfully.")
#                 return redirect('donation_status')
#             except IntegrityError as e:
#                 messages.error(request, "Failed to record donation. Please try again.")
#                 logger.error(f"IntegrityError: {e}")
#                 return redirect('donate_blood', camp_id=camp_id)
#         else:
#             messages.error(request, "Please provide all required details.")
#             return redirect('donate_blood', camp_id=camp_id)

#     form = BloodDonationForm()
#     return render(request, 'blood_donation/donation_blood.html', {'form': form, 'donor_profile': donor_profile})


@user_passes_test(is_not_admin, login_url='admin_dashboard')
@login_required(login_url='/login')
def donate_blood(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.user_type == 'admin':
        messages.error(request, 'Admins cannot donate blood.')
        return redirect('home')

    if user_profile.user_type == 'recipient':
        query_params = urlencode({
            'message': 'You are logged in as a recipient, so you cannot donate blood.',
            'link_text': 'Go to Request Blood',
            'link_url': '/request_blood'
        })
        return HttpResponseRedirect(f'/message/?{query_params}')

    try:
        donor_profile = DonorProfile.objects.get(user=user_profile)
    except DonorProfile.DoesNotExist:
        messages.error(request, "You need to complete your donor profile first.")
        return redirect('donor_profile', user_profile_id=user_profile.id)

    if donor_profile.age < 18 or donor_profile.age > 55:
        messages.error(request, "You must be between 18 and 55 years old to donate blood.")
        return redirect('donation_status')

    upcoming_camps = DonationCamp.objects.filter(date__gte=timezone.now()).exists()
    if not upcoming_camps:
        messages.error(request, "No donation camps are available at the moment.")
        return redirect('donation_status')

    three_months_ago = timezone.now() - timedelta(days=90)
    last_donation = BloodDonation.objects.filter(user=donor_profile, donation_date__gte=three_months_ago).first()
    if last_donation:
        messages.error(request, "You cannot donate blood more than once in a 3-month period.")
        return redirect('donation_status')

    if request.method == 'POST':
        form = BloodDonationForm(request.POST)
        if form.is_valid():
            blood_donation = form.save(commit=False)
            blood_donation.user = donor_profile
            try:
                blood_donation.save()
                messages.success(request, "Donation recorded successfully.")
                return redirect('donation_status')
            except IntegrityError as e:
                messages.error(request, "Failed to record donation. Please try again.")
                logger.error(f"IntegrityError: {e}")
                return redirect('donate_blood')
        else:
            # Handle specific errors
            for field, errors in form.errors.items():
                if field == 'donation_date':
                    messages.error(request, "Error in donation_date: Enter a valid date.")
                elif field == 'status':
                    messages.error(request, "Error in status: This field is required.")
                else:
                    for error in errors:
                        messages.error(request, f"Error in {field}: {error}")

            return render(request, 'blood_donation/donation_blood.html', {'form': form, 'donor_profile': donor_profile})

    form = BloodDonationForm()
    return render(request, 'blood_donation/donation_blood.html', {'form': form, 'donor_profile': donor_profile})



@login_required(login_url='/login')
def donation_status(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    try:
        donor_profile = DonorProfile.objects.get(user=user_profile)
        donations = BloodDonation.objects.filter(user=donor_profile)
    except DonorProfile.DoesNotExist:
        donor_profile = None
        donations = []

    # Pass donor_profile data to the template if needed
    return render(request, 'blood_donation/donation_status.html', {
        'donations': donations,
        'donor_profile': donor_profile  # Pass donor_profile to template
    })


@user_passes_test(is_not_admin, login_url='admin_dashboard')
@login_required(login_url='/login')
def request_blood(request):
    # In request_blood view:
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'donor':
        query_params = urlencode({
            'message': 'You are logged in as a donor, so you cannot request blood.',
            'link_text': 'Go to Donate Blood',
            'link_url': '/donate_blood'
        })
        return HttpResponseRedirect(f'/message/?{query_params}')

    try:
        recipient_profile = RecipientProfile.objects.get(user=user_profile)
    except RecipientProfile.DoesNotExist:
        messages.error(request, "You need to complete your recipient profile first.")
        return redirect('recipient_profile', user_profile_id=user_profile.id)

    active_request = BloodRequest.objects.filter(
        user=user_profile,
        status='Pending'  # Default status for new requests
    )

    if active_request.exists():
        messages.info(request, "You already have an active or incomplete blood request.")
        return redirect('request_status')

    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        required_date = request.POST.get('required_date')
        quantity = request.POST.get('quantity')

        if not quantity or not quantity.isdigit():
            messages.error(request, "Please enter a valid quantity.")
            return redirect('request_blood')

        quantity = int(quantity)

        BloodRequest.objects.create(
            user=user_profile,  # Ensure this is a UserProfile instance
            blood_group=blood_group,
            required_date=required_date,
            quantity=quantity,
            status='Pending'  # Default status
        )
        messages.success(request, "Blood request recorded successfully.")
        return redirect('request_status')

    blood_group_choices = BloodRequest.BLOOD_GROUP_CHOICES
    return render(request, 'blood_donation/request_blood.html', {
        'user': request.user,
        'user_profile': user_profile,
        'recipient_profile': recipient_profile,
        'blood_group_choices': blood_group_choices
    })



@login_required(login_url='/login')
def request_status(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        recipient_requests = BloodRequest.objects.filter(user=user_profile)
    except UserProfile.DoesNotExist:
        recipient_requests = []

    return render(request, 'blood_donation/request_status.html', {
        'recipient_requests': recipient_requests,
    })

@staff_member_required
def add_donation_camp(request):
    if request.method == 'POST':
        form = DonationCampForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Donation camp added successfully.")
            return redirect('donation_camp_list')
    else:
        form = DonationCampForm()

    return render(request, 'admin/add_donation_camp.html', {'form': form})

@login_required
def donation_camp_list(request):
    camps = DonationCamp.objects.all()
    return render(request, 'donation/camp_list.html', {'camps': camps})



@login_required
def donation_camp_detail(request, camp_id):
    camp = get_object_or_404(DonationCamp, id=camp_id)
    user_profile = request.user.donorprofile
    existing_donation = BloodDonation.objects.filter(donor=user_profile, camp=camp).first()
    
    if request.method == 'POST' and not existing_donation:
        BloodDonation.objects.create(donor=user_profile, camp=camp, blood_group=user_profile.blood_group)
        return redirect('donation_camp_detail', camp_id=camp.id)
    
    return render(request, 'donation/camp_detail.html', {'camp': camp, 'existing_donation': existing_donation})

# @login_required
# def generate_certificate(request, donation_id):
#     donation = get_object_or_404(BloodDonation, id=donation_id)
#     if donation.status == 'Completed':
#         donor_profile = donation.donor
#         certificate_html = render_to_string('certificate_template.html', {
#             'donor': donor_profile,
#             'camp': donation.camp,
#             'blood_group': donation.blood_group,
#         })
        
#         pdf_file = HTML(string=certificate_html).write_pdf()
#         response = HttpResponse(pdf_file, content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="certificate_{donation_id}.pdf"'
        
#         return response
#     else:
#         return redirect('donation_camp_detail', camp_id=donation.camp.id)

def send_registration_notification(donor_profile, camp, donation_date):
    subject = 'Registration Confirmation for Blood Donation Camp'
    if donor_profile.user:
        username = donor_profile.user.username
    else:
        username = "Donor"

    message = f"Dear {username},\n\n"

    recipient_list = [donor_profile.user.email]
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )

# @login_required
# def donation_status(request):
#     # Get the UserProfile for the currently logged-in user
#     user_profile = get_object_or_404(UserProfile, user=request.user)

#     # Get the DonorProfile associated with the UserProfile
#     donor_profile = get_object_or_404(DonorProfile, user=user_profile)

#     # Now use the DonorProfile instance to filter BloodDonation objects
#     donor_donations = BloodDonation.objects.filter(user=donor_profile)

#     context = {
#         'donor_donations': donor_donations,
#     }
#     return render(request, 'donation/status.html', context)

def contact_success(request):
    return render(request, 'contact_success.html')

@login_required
def edit_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    if request.method == 'POST':
        # Directly update model fields based on POST data
        blood_request.blood_group = request.POST.get('blood_group')
        blood_request.required_date = request.POST.get('required_date')
        blood_request.quantity = request.POST.get('quantity')
        blood_request.status = request.POST.get('status')
        blood_request.save()
        return redirect('request_status')  # Redirect to the request status page after saving
    else:
        # Render the edit form with existing request data
        return render(request, 'edit_request.html', {'blood_request': blood_request})
    
@login_required
def delete_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    if request.method == 'POST':
        blood_request.delete()
        return redirect('request_status')  # Redirect to the request status page after deletion

    return render(request, 'delete_request_confirm.html', {'blood_request': blood_request})


@login_required
def edit_donation(request, donation_id):
    donation = get_object_or_404(BloodDonation, id=donation_id)

    if request.method == 'POST':
        # Directly update model fields based on POST data
        donation.blood_group = request.POST.get('blood_group')
        donation.donation_date = request.POST.get('donation_date')
        donation.status = request.POST.get('status')
        donation.save()
        return redirect('donation_status')  # Redirect to the donation status page after saving
    else:
        # Render the edit form with existing donation data
        return render(request, 'edit_donation.html', {'donation': donation})

@login_required
def delete_donation(request, donation_id):
    donation = get_object_or_404(BloodDonation, id=donation_id)

    if request.method == 'POST':
        donation.delete()
        return redirect('donation_status')  # Redirect to the donation status page after deletion

    return render(request, 'delete_donation_confirm.html', {'donation': donation})

def message_page(request):
    # Extract query parameters
    message = request.GET.get('message', 'Default message')
    link_text = request.GET.get('link_text', 'Go back')
    link_url = request.GET.get('link_url', '/')
    
    return render(request, 'message_page.html', {
        'message': message,
        'link_text': link_text,
        'link_url': link_url
    })



# View for Users to Search Blood Banks
def search_blood_bank(request):
    query = request.GET.get('q', '').strip()
    if query:
        blood_banks = BloodBank.objects.filter(name__icontains=query)
    else:
        blood_banks = BloodBank.objects.all()
    return render(request, 'blood_bank/search_blood_bank.html', {'blood_banks': blood_banks, 'query': query})

@staff_member_required
def add_blood_bank(request):
    if request.method == 'POST':
        form = BloodBankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blood_bank_list')  # Redirect to a list view or success page
    else:
        form = BloodBankForm()
    
    return render(request, 'blood_bank/add_blood_bank.html', {'form': form})

def blood_bank_list(request):
    blood_banks = BloodBank.objects.all()
    return render(request, 'blood_bank/blood_bank_list.html', {'blood_banks': blood_banks})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')


@login_required(login_url='/login')
def restricted_view(request):
    if request.user.userprofile.user_type != 'admin':
        return HttpResponseNotFound('Page not found')  # Handle as per your needs
    return render(request, 'admin_only.html')


def donation_list_view(request):
    donations = BloodDonation.objects.select_related('user').all()
    context = {'donations': donations}
    return render(request, 'donor/donation_list.html', context)


def request_list_view(request):
    recipient_requests = BloodRequest.objects.all()  # Ensure this is the correct query
    context = {
        'recipient_requests': recipient_requests
    }
    return render(request, 'donor/request_list.html', context)


def donor_list_view(request):
    donors = DonorProfile.objects.all()
    context = {'donors': donors}
    return render(request, 'donor/donor_list.html', context)

def recipient_list_view(request):
    recipients = RecipientProfile.objects.all()
    context = {'recipients': recipients}
    return render(request, 'donor/recipient_list.html', context)


def edit_donor_view(request, donor_id):
    donor = get_object_or_404(DonorProfile, id=donor_id)
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect(reverse('donor_list'))
    else:
        form = DonorProfileForm(instance=donor)
    return render(request, 'edit_donor.html', {'form': form, 'donor': donor})

def delete_donor_view(request, donor_id):
    donor = get_object_or_404(DonorProfile, id=donor_id)
    if request.method == 'POST':
        donor.delete()
        return redirect(reverse('donor_list'))
    return render(request, 'delete_donor.html', {'donor': donor})


def edit_recipient_view(request, recipient_id):
    recipient = get_object_or_404(RecipientProfile, id=recipient_id)
    if request.method == 'POST':
        form = RecipientProfileForm(request.POST, instance=recipient)
        if form.is_valid():
            form.save()
            return redirect(reverse('recipient_list'))
    else:
        form = RecipientProfileForm(instance=recipient)
    return render(request, 'edit_recipient.html', {'form': form, 'recipient': recipient})

def delete_recipient_view(request, recipient_id):
    recipient = get_object_or_404(RecipientProfile, id=recipient_id)
    if request.method == 'POST':
        recipient.delete()
        return redirect(reverse('recipient_list'))
    return render(request, 'delete_recipient.html', {'recipient': recipient})


def edit_donation_camp_view(request, camp_id):
    camp = get_object_or_404(DonationCamp, id=camp_id)

    if request.method == 'POST':
        form = DonationCampForm(request.POST, instance=camp)
        if form.is_valid():
            form.save()
            return redirect('donation_camp_list')  # Redirect to the list view or another page after saving
    else:
        form = DonationCampForm(instance=camp)

    return render(request, 'donor/edit_donation_camp.html', {'form': form})


def delete_donation_camp_view(request, camp_id):
    camp = get_object_or_404(DonationCamp, id=camp_id)

    if request.method == 'POST':
        camp.delete()
        return redirect('donation_camp_list')  # Redirect to the list view or another page after deletion

    return render(request, 'donor/confirm_delete.html', {'camp': camp})


