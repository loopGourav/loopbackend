"""
All user related common module
"""

# auth user model tables
from django.contrib.auth.models import User
from users.models import UserProfile


def get_auth_user_instance(filter_req_data):
    """
    This "get_auth_user_instance" function used to get the auth user instance 
    according to filter request data
    params:
        ex: filter_req_data: {'id': 1}
    return: query_instance
    """
    try:
        return User.objects.get(**filter_req_data)
    except User.DoesNotExist:
        return None


def get_user_profile_instance(filter_req_data):
    """
    This "get_user_profile_instance" function used to get the user profile instance 
    according to filter request data
    params:
        ex: filter_req_data: {'id': 1}
    return: query_instance
    """
    try:
        return UserProfile.objects.get(**filter_req_data)
    except UserProfile.DoesNotExist:
        return None


def update_user_profile_details(filter_req_data, update_req_data):
    """
    This "update_user_profile_details" function used to update the all 
    user profile related data using update query data
    """
    return UserProfile.objects.filter(**filter_req_data).update(**update_req_data)



