"""UserOTPSystem
Created at 21 August 2021 by Gourav Sharma (^_^)
This user otp system used to generate the otp for a customer for verified account and 
also used with forgot verification
"""

import random

from datetime import datetime
from datetime import timedelta

from helper.messages import MSG
from helper.utils import get_auth_service_type
from helper.utils import json_dict_parser
from users.models import UserProfile, TwoFactorAuthentication
from users.user_modules.authenticate_user_login import authenticate_with_token


def get_the_otp():
    """get_the_otp
    this get_the_otp() methods used to generate the 6 digits random number
    for customer otp
    """
    return random.randint(100000, 999999)


class MutualOTPSystem:
    """
    MutualOTPSystem
    This MutualOTPSystem() class Module help the generate and sent the 6 digit otp for 
    customers user to authenticate valid users
    Methods:
        generate_otp_and_send_notification()
    """

    def __init__(self, user_instance, service_name):
        self.user_instance = user_instance
        self.service_name = service_name
        self.sms_otp_expiry = timedelta(minutes=30)
        self.errors_result_dict = {
            "message": "user instance not valid for otp",
            "status": False
        }

    def __call__(self):
        if not self.user_instance:
            return self.errors_result_dict
        return self.generate_otp_and_send_notification()

    def generate_otp_and_send_notification(self):
        """generate_otp_and_send_notification
        This generate_otp_and_send_notification() method used to sent the notification for 
        user and generate the otp with link by user db
        In this method we used to customize the self otp with entry in db 
        models to track the how many sent notification
        and verified users
        """
        random_otp_number = get_the_otp()
        try:
            otp_success_status = 'successful' if sms_trigger_status else 'not_delivered'
        except Exception as msg:
            print(msg)
            otp_success_status = 'not_delivered'

        create_otp_instance = TwoFactorAuthentication.objects.create(
            user=self.user_instance,
            otp=random_otp_number,
            otp_status=otp_success_status,
            auth_type=get_auth_service_type(self.user_instance.username),
            expired_datetime=datetime.now() + self.sms_otp_expiry
        )

        if create_otp_instance:
            return {
                'status': True,
                'message': MSG['SUCCESS'],
                'data': {'otp': random_otp_number},
            }
        else:
            return {
                'status': False,
                'message': MSG['OTP_FAILED'],
                'data': {},
            }


class OTPVerification:
    """
    OTPVerification
    This OTPVerification class Module used to verification the otp process
    Methods:
        otp_verification_module()
    """

    def __init__(self, **kwargs):
        self.otp = kwargs.get('otp')
        self.auth_user_id = kwargs.get('auth_user_id')
        self.current_date_time = datetime.now()
        self.source_type = kwargs.get('source_type', 'API')

    def __call__(self):
        return self.otp_verification_module()

    def otp_verification_module(self):
        """otp_verification_module
        this otp_verification_module() methods used to verification of otp 
        user validate mobile number is correct or not
        """
        _two_factor_instance = TwoFactorAuthentication.objects.filter(
            created_at__lte=self.current_date_time,
            expired_datetime__gte=self.current_date_time,
            user_id=self.auth_user_id).last()

        # OTP Expired Error message
        if not _two_factor_instance:
            return False, {}, MSG['OTP_EXPIRED']

        # OTP match conditions with
        # update the status of customer user
        if int(_two_factor_instance.otp) == int(self.otp):
            _two_factor_instance.is_verified = True
            _two_factor_instance.save()
            if self.source_type == 'API':
                return authenticate_with_token(self.auth_user_id)
            return True, {}, MSG['DONE']

        # OTP Mismatch with
        # warning message
        return False, {}, MSG['OTP_MISMATCH']
