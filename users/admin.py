from django.contrib import admin

# Register your models here.

from users.models import UserProfile
from users.models import TwoFactorAuthentication


class TwoFactorAuthenticationAdmin(admin.ModelAdmin):
    """
    TwoFactorAuthenticationAdmin : search, filter and display in admin panel..
    """

    ordering = ('-created_at',)

    search_fields = [
        'user__email',
        'user__mobile_no',
        'user__auth__username'
    ]
    list_filter = [
        'otp_status',
        'auth_type',
        'created_at',
        'expired_datetime',
    ]
    list_display = [
        'get_user_name',
        'otp',
        'otp_status',
        'auth_type',
        'created_at',
        'expired_datetime'
    ]
    readonly_fields = [
        'get_user_name',
        'otp',
        'otp_status',
        'auth_type',
        'created_at',
        'expired_datetime'
    ]

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        """
        has_delete_permission: used to remove delete functionalty in admin panel.
        """
        return False

    def has_add_permission(self, request, obj=None):
        """
        has_add_permission: used to add and not add permission in adin panel.
        """
        return False


# Registered TwoFactorAuthenticationAdmin table ..


admin.site.register(UserProfile)
admin.site.register(TwoFactorAuthentication, TwoFactorAuthenticationAdmin)
