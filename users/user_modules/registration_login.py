"""RegistrationLoginModule
created at 21 august 2021 by Gourav Sharma (^_^)
This RegistrationLoginModule() used to manage all login cases to help the login a new user or old user
"""

import random
import string
# from django.utils.text import slugify
from random import choice
from string import digits, ascii_lowercase

# auth user model tables
from django.contrib.auth.models import User

from users.models import UserProfile

from helper.utils import mobile_number_validate, is_valid_email
from helper.messages import MSG
from users.user_modules.user_otp_generation import MutualOTPSystem


class RegistrationLoginModule:
    """
    RegistrationLoginModule
    """

    def __init__(self, **kwargs):
        self.username = kwargs.get('username', None)
        self.device_type = kwargs.get('device_type', None)
        self.auth_type_username = 'email'
        self.login_user_type = 'native'
        self.user_type = 'customer'
        self.service_name = 'registration'
        self.source_type = kwargs.get('source_type', 'API')
        self.registration_login_source = kwargs.get('source_type', 'API')
        self.otp_sent_status = False
        self.random_password_key = None

    def validate_username_parameter(self):
        """
        This "validate_username_parameter" method used to validate the username field 
        for check username field is mobile number and email
        """
        mobile_validate_status = mobile_number_validate(self.username)
        email_validate_status = is_valid_email(self.username)
        if mobile_validate_status is False and email_validate_status is False:
            return False
        self.auth_type_username = (
            'phone_no'
            if mobile_validate_status is True else 'email')

        # all result success
        return True

    def is_user_already_exist(self):
        """
        This is_user_already_exist() method used to check 
        the user already exist or not in our application system
        """
        try:
            return User.objects.get(username=self.username)
        except User.DoesNotExist:
            return None

    def random_password_generate(self):
        """
        this "random_password_generate" method used to generate 
        the random string password for store new user
        actlly this random password used for dummy password because password is mandatory
        but our system not generate password for registration time user, password generate 
        after otp verification for new user so 
        we used random password function for create auth user
        """
        self.random_password_key = ''.join(
            random.choice(string.ascii_uppercase + 3 * string.digits)
            for i in range(10)
        )

    def create_auth_user(self):
        """
        This "create_auth_user" method used to create a new auth user to authenticate 
        with django auth and jwt token system 
        """
        return User.objects.create_user(
            username=self.username,
            password=self.random_password_key,
            is_staff=False, is_active=False, is_superuser=False)

    def user_profile_with_otp_generation(self, auth_user_instance):
        """
        This "user_profile_with_otp_generation" method used to create user 
        profile with park auth user id
        """
        create_user_profile_data = {
            'user_type': self.user_type,
            'device_type': self.device_type,
            'login_type': self.login_user_type,
            'auth_user_id': auth_user_instance.id,
            self.auth_type_username: self.username,
            'random_password_key': self.random_password_key,
            'registration_source': 'API' if self.source_type == 'API' else 'TEMPLATE',
            'created_by': auth_user_instance
        }
        user_profile_create = UserProfile.objects.create(
            **create_user_profile_data)
        if not user_profile_create:
            return False, MSG['USER_NOT_CREATED'], None
        mutual_otp_instance = MutualOTPSystem(auth_user_instance,
                                              self.service_name)
        otp_status_data = mutual_otp_instance()
        if otp_status_data['status']:
            self.otp_sent_status = True
            return True, otp_status_data['message'], str(auth_user_instance.id)
        return False, otp_status_data['message'], str(auth_user_instance.id)

    def registration_login_process(self):
        """
        This method used to create a new user instance and if user already exist with 
        valid credentials so it will redirect.
        params: self.username
        in username variable have 2 types of data values (email/mobile)
        return:
        """
        if not self.validate_username_parameter():
            return {'status': False, 'message': MSG['USERNAME_NOT_VALID'], 'data': {}}
        # old user process
        already_exist_instance = self.is_user_already_exist()
        if already_exist_instance:
            if self.source_type == 'API':
                mutual_otp_instance = MutualOTPSystem(
                    already_exist_instance,
                    self.service_name)
                otp_status_data = mutual_otp_instance()
                self.otp_sent_status = True
            return {
                'status': True,
                'message': MSG['OLD_USER_LOGIN'],
                'data': {
                    'otp_sent': self.otp_sent_status,
                    'user_id': str(already_exist_instance.id),
                    'is_new_user': False
                },
            }
        # create new user process
        self.random_password_generate()
        auth_user_instance = self.create_auth_user()
        if not auth_user_instance:
            # auth user not found
            # result response dict
            return {
                'status': False,
                'message': MSG['AUTH_USER_NOT_CREATE'],
                'data': {}
            }
        # final response dict

        print('auth_user_instance')
        print(auth_user_instance)
        status, message, user_id = self.user_profile_with_otp_generation(
            auth_user_instance)
        if not status:
            return {'status': False, 'message': message}
        return {
            'status': True,
            'message': message,
            'data': {
                'user_id': user_id,
                'otp_sent': self.otp_sent_status,
                'is_new_user': True
            }
        }
