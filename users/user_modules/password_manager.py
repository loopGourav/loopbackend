"""
PasswordManagerModule
Created At 24 August 2021 by Gourav Sharma(^_^)
This module used to generate and verification the auth user password as a our system customers
"""
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from helper.constants import USER_REDIRECT_PATH
from helper.messages import MSG
from helper.utils import json_dict_parser
from helper.controller import BackendQueryController

from users.models import UserProfile
from users.user_modules.authenticate_user_login import authenticate_login_user


class UserPasswordManager:
    """
    UserPasswordManager
    24 August 2021 by Gourav Sharma (^_^)
    module: generate and verification the auth user password as a PASSWORD_CREATED_SUCCESSour system customers
    params: 
        auth_user_id
        password
        confirm_password
    methods:
        password_generation()
        password_verification()
    """

    def __init__(self, **kwargs):
        self.request_instance = kwargs.get('request_instance', None)
        self.auth_user_id = kwargs.get('auth_user_id', None)
        self.password = kwargs.get('password', None)
        self.confirm_password = kwargs.get('confirm_password', None)
        self.auth_user_instance = None
        self.service_type = kwargs.get('service_type', None)

    def is_pass_valid(self):
        """
        This is_pass_valid method used to check password is valid or not 
        as validation type level
        """
        return False if self.confirm_password != self.password else True

    def update_user_password(self):
        """
        This "update_user_password" method used to update the django auth user password
        """
        self.auth_user_instance.set_password(self.confirm_password)
        self.auth_user_instance.save()

    def login_with_status(self):
        """
        This "login_with_status" method used to create login function with update all user 
        related status to help the login django session auth
        """
        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': self.auth_user_instance.id})
        _auth_user_instance = _backend_controller_instance.get_query_instance()
        if not _auth_user_instance:
            return json_dict_parser(
                MSG['AUTH_USER_NOT_FOUND'], {}, False)

        _auth_user_instance.is_active = True
        _auth_user_instance.save()

        # get user profile instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=UserProfile,
            filter_req_data={'auth_user': _auth_user_instance})
        _user_profile_instance = _backend_controller_instance.get_query_instance()
        if not _user_profile_instance:
            return json_dict_parser(
                MSG['USER_PROFILE_NOT_GENERATED'], {}, False)

        # update user profile query using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=UserProfile,
            filter_req_data={'id': _user_profile_instance.id},
            input_req_data={'is_password_created': True,
                            'is_active': True}
        )
        user_update_status = _backend_controller_instance.update_query_set()
        if not user_update_status:
            return json_dict_parser(MSG['PROFILE_NOT_UPDATE'], {}, False)
        login_user_status = authenticate_login_user(
            self.request_instance,
            {'username': _auth_user_instance.username,
             'password': self.confirm_password})
        if login_user_status:
            return json_dict_parser(MSG['PASSWORD_CREATED_SUCCESS'], {}, True)
        return json_dict_parser(MSG['LOGIN_ERROR'], {}, False)

    def password_generation(self):
        """
        This "password_generation" method used to generate the user password for new users
        """
        if not self.is_pass_valid():
            return json_dict_parser(
                MSG['PASSWORD_NOT_MATCH'],
                {}, True)

        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': self.auth_user_id})
        self.auth_user_instance = _backend_controller_instance.get_query_instance()
        if self.auth_user_instance:
            self.update_user_password()
            if self.service_type == '__REGISTRATION__':
                return self.login_with_status()
            return json_dict_parser(MSG['PASSWORD_CREATED_SUCCESS'], {}, True)
        return json_dict_parser(
            MSG['AUTH_USER_NOT_FOUND'],
            {},
            True)

    def profile_redirect_path(self):
        """
        This "profile_redirect_path" method used to get the profile url 
        path according to user which state
        """
        # get user profile instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=UserProfile,
            filter_req_data={'auth_user': self.auth_user_instance})
        _user_profile_instance = _backend_controller_instance.get_query_instance()
        if _user_profile_instance:
            if _user_profile_instance.is_profile_completed is True:
                return USER_REDIRECT_PATH['HOME']
            if _user_profile_instance.is_first_step_completed is False:
                return USER_REDIRECT_PATH['FIRST']
            if _user_profile_instance.is_second_step_completed is False:
                return USER_REDIRECT_PATH['SECOND']
            if _user_profile_instance.is_third_step_completed is False:
                return USER_REDIRECT_PATH['THIRD']
        return USER_REDIRECT_PATH['LOGOUT']

    def password_verification(self):
        """
        This "password_generation" method used to generate the user password for new users
        """
        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': self.auth_user_id})
        self.auth_user_instance = _backend_controller_instance.get_query_instance()
        if not self.auth_user_instance:
            return json_dict_parser(MSG['AUTH_USER_NOT_FOUND'], {}, False)

        # login process and validate
        # the password with correct user
        login_user_status = authenticate_login_user(
            self.request_instance,
            {'username': self.auth_user_instance.username,
             'password': self.password})
        if login_user_status:
            return json_dict_parser(
                MSG['PASSWORD_LOGIN_SUCCESS'],
                {'redirect_user_url': self.profile_redirect_path()}, True)
        return json_dict_parser(MSG['LOGIN_ERROR'], {}, False)
