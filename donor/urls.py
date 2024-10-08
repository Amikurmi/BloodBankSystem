from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('donor_profile/<int:user_profile_id>/', views.donor_profile, name='donor_profile'),
    # path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('recipient_profile/<int:user_profile_id>/', views.recipient_profile, name='recipient_profile'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('donor_dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('recipient_dashboard/', views.recipient_dashboard, name='recipient_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('donate_blood/', views.donate_blood, name='donate_blood'),
    path('donation_status/', views.donation_status, name='donation_status'),
    path('request_blood/', views.request_blood, name='request_blood'),
    path('request_status/', views.request_status, name='request_status'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('edit_request/<int:request_id>/', views.edit_request, name='edit_request'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('edit_donation/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('delete_donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('message/', views.message_page, name='message_page'),
    path('add_blood_bank/', views.add_blood_bank, name='add_blood_bank'),
    path('search_blood_bank/', views.search_blood_bank, name='search_blood_bank'),
    path('blood_bank_list/', views.blood_bank_list, name='blood_bank_list'),
    path('camps/', views.donation_camp_list, name='donation_camp_list'),
    path('camps/edit/<int:camp_id>/', views.edit_donation_camp_view, name='edit_camp'),
    path('camps/delete/<int:camp_id>/', views.delete_donation_camp_view, name='delete_camp'),
    path('camps/<int:pk>/', views.donation_camp_detail, name='donation_camp_detail'),
    path('camps/add/', views.add_donation_camp, name='add_donation_camp'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('donations/', views.donation_list_view, name='donation_list'),
    path('requests/', views.request_list_view, name='request_list'),
    path('recipients/', views.recipient_list_view, name='recipient_list'),
    path('donors/', views.donor_list_view, name='donor_list'),
    path('donors/edit/<int:donor_id>/', views.edit_donor_view, name='edit_donor'),
    path('donors/delete/<int:donor_id>/', views.delete_donor_view, name='delete_donor'),
    path('recipients/edit/<int:recipient_id>/', views.edit_recipient_view, name='edit_recipient'),
    path('recipients/delete/<int:recipient_id>/', views.delete_recipient_view, name='delete_recipient'),
    # path('certificate/<int:donation_id>/', views.generate_certificate, name='generate_certificate'),
    # path('donate_blood/<int:camp_id>/', views.donate_blood, name='donate_blood'),


    
]