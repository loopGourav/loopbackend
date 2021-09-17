"""
UserProfileTable
created at 15 august 2021 by GouravSharma(^_^)
This UserProfileTable used to maintain user customer profile table using onetoone field
with auth user table to help to authenticate the auth user
https://stackoverflow.com/questions/31670393/
difference-between-foreignkey-and-extending-the-user-class-model-in-django
"""

from django.db import models

# auth user model tables
from django.contrib.auth.models import User

# helper abstract user models tables
from helper.models import CreateUpdateByAbstractModel
from helper.models import DateAbstractModel
from helper.models import StatusAbstractModel
from helper.models import LocationMaster

from configurations.models import CityMaster

from helper.constants import LOGIN_USER_TYPE
from helper.constants import DEVICE_TYPE
from helper.constants import USER_TYPE
from helper.constants import OTP_STATUS
from helper.constants import SERVICE_TYPE
from helper.constants import REGISTRATION_SOURCE


# Create your models here.


class UserProfile(CreateUpdateByAbstractModel,
                  DateAbstractModel,
                  StatusAbstractModel,
                  LocationMaster):
    """
    UserProfileDetails
    This UserProfileDetails models store all user profile detail with mapping auth user models
    """
    # authentication related parameters fields
    email = models.EmailField(null=True, blank=True)
    isd = models.CharField(
        max_length=10, null=True,
        blank=True, verbose_name='ISD')
    phone_no = models.CharField(
        max_length=20, null=True,
        blank=True, verbose_name='Mobile No.')

    # profile pic and short intro parameters fields
    profile_picture = models.FileField(
        upload_to='users/profile_pic', null=True, blank=True)
    short_intro = models.TextField(null=True, blank=True)

    # specification parameters fields
    price = models.FloatField(null=True, blank=True)
    talent = models.CharField(max_length=100, null=True, blank=True)
    interest = models.CharField(max_length=100, null=True, blank=True)

    # basic profile parameters fields
    your_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    dob = models.CharField(max_length=10, null=True, blank=True)

    # device level parameters fields
    device_type = models.CharField(
        max_length=100, choices=DEVICE_TYPE, null=True, blank=True)
    login_type = models.CharField(
        max_length=100, choices=LOGIN_USER_TYPE, null=True, blank=True)
    user_type = models.CharField(
        max_length=100, choices=USER_TYPE, null=True, blank=True)
    device_id = models.CharField(max_length=225, null=True, blank=True)
    random_password_key = models.CharField(
        max_length=255, null=True, blank=True)
    registration_source = models.CharField(
        max_length=100, choices=REGISTRATION_SOURCE)

    is_otp_verified = models.BooleanField(default=False)
    is_password_created = models.BooleanField(default=False)
    is_first_step_completed = models.BooleanField(default=False)
    is_second_step_completed = models.BooleanField(default=False)
    is_third_step_completed = models.BooleanField(default=False)
    is_profile_completed = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    auth_user = models.OneToOneField(
        User,
        related_name='auth_user',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profile'
        db_table = 'user_profile'

    def __str__(self):
        return str(self.auth_user.username)


class TwoFactorAuthentication(models.Model):
    """
    mobile and email authentication module
    """
    otp = models.PositiveIntegerField()
    otp_status = models.CharField(
        max_length=20,
        verbose_name='OTP Status',
        choices=OTP_STATUS)
    auth_type = models.CharField(max_length=20, choices=SERVICE_TYPE)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created At')
    expired_datetime = models.DateTimeField(verbose_name="Expired At")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Two Factor Authentication'
        verbose_name_plural = 'Two Factor Authentication'
        db_table = 'two_factor_authentication'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.otp)

    def get_user_name(self):
        """
        created at 2021-08-31 by Gourav Sharma (^_^) get_user_name
        This "get_user_name" method used to get the username to get the username
        return: (username)
        """
        if self.user:
            return str(self.user.username) if self.user.username else '-'
        else:
            return '-'

    get_user_name.short_description = 'Email/ MobileNo'
