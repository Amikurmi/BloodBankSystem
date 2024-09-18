from django.contrib import admin
from .models import UserProfile, BloodDonation, RecipientProfile, BloodRequest, BloodBank, DonationCamp, DonorRegistration, DonorProfile
from django.core.mail import send_mail

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    search_fields = ('user__username', 'user_type')

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'age', 'contact_number')
    search_fields = ('user__user__username', 'first_name', 'last_name')

@admin.register(RecipientProfile)
class RecipientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'age', 'contact_number', 'address')
    search_fields = ('user__user__username', 'first_name', 'last_name')

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number', 'email')
    search_fields = ('name', 'address', 'contact_number')

        
class RegistrationInline(admin.TabularInline):
    model = DonorRegistration
    extra = 1
    readonly_fields = ('user',)
    can_delete = False

@admin.register(DonationCamp)
class DonationCampAdmin(admin.ModelAdmin):
    list_display = ('name', 'date','place')
    search_fields = ('name', 'place')
    list_filter = ('date', 'place')
    date_hierarchy = 'date'
    ordering = ('-date', 'name')
    inlines = [RegistrationInline]

def send_notification(modeladmin, request, queryset):
    for obj in queryset:
        user_email = obj.user.user.email if obj.user.user.email else 'from@example.com'
        send_mail(
            'Notification',
            f'You have been registered for {obj.camp.name} on {obj.camp.date} at {obj.camp.time}. Location: {obj.camp.place}.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
    modeladmin.message_user(request, "Notifications sent successfully.")

send_notification.short_description = 'Send notification to selected registrations'

class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'donation_date', 'status')

    def save_model(self, request, obj, form, change):
        if not request.user.is_staff and 'status' in form.changed_data:
            raise PermissionError("Only admins can change the status.")
        super().save_model(request, obj, form, change)

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'required_date', 'status')

    def save_model(self, request, obj, form, change):
        if not request.user.is_staff and 'status' in form.changed_data:
            raise PermissionError("Only admins can change the status.")
        super().save_model(request, obj, form, change)

admin.site.register(BloodDonation, BloodDonationAdmin)
admin.site.register(BloodRequest, BloodRequestAdmin)



