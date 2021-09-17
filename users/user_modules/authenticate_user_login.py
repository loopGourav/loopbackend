import requests

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.models import User
from users.models import UserProfile
from helper.controller import BackendQueryController

from back_end.settings.development import BASE_URL_PATH


def authenticate_with_token(auth_user_id):
    """
    This "authenticate_with_token" function used for APIs level authentication token
    authenticate_with_token
    This "authenticate_with_token" function used to generate the token with login data 
    and requests api using JWT APIs
    """
    # get auth user instance using "BackendQueryController"
    # with passing parameter filter data
    _backend_controller_instance = BackendQueryController(
        model_name=User,
        filter_req_data={'id': auth_user_id})
    auth_user_instance = _backend_controller_instance.get_query_instance()

    if not auth_user_instance:
        False, {}, 'AUTH.USER.NOT.FOUND'
    auth_user_instance.is_active = True
    auth_user_instance.save()

    # user profile instance
    # get the user profile isntance using "BackendQueryController" 
    # with passing parameters
    _backend_controller_instance = BackendQueryController(
        model_name=UserProfile,
        filter_req_data={'auth_user_id': auth_user_id})
    user_profile_instance = _backend_controller_instance.get_query_instance()
    if not user_profile_instance:
        return False, {}, 'User Not Foud'

    # JWT Token
    # authenticate the jwt token with using user 
    # account credentials (username/password)
    response = requests.post(
        ''.join([BASE_URL_PATH, '/api/token/']),
        data={
            'username': user_profile_instance.auth_user.username,
            'password': user_profile_instance.random_password_key
        }
    )
    if response.status_code == 200:
        return True, {
            'access_code': response.json()['access'],
            'is_otp_verified': user_profile_instance.is_otp_verified,
            'is_first_step_completed': user_profile_instance.is_first_step_completed,
            'is_second_step_completed': user_profile_instance.is_second_step_completed,
            'is_third_step_completed': user_profile_instance.is_third_step_completed,
            'is_profile_completed': user_profile_instance.is_profile_completed
        }, 'DONE'
    False, {}, 'JWT.EXCEPTION.ERROR'


def authenticate_login_user(request, authenticate_data):
    """
    this "authenticate_login_user" function used for web templates authentications
    This "authenticate_login_user" method used to login and authenticate the auth user
    """
    auth_user_authenticated = authenticate(**authenticate_data)
    if auth_user_authenticated is not None:
        if auth_user_authenticated.is_active:
            login(request, auth_user_authenticated)
            return True
        return False
    return False
