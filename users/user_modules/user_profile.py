"""
UserProfile module
"""

from django.contrib.auth.models import User

from users.models import UserProfile
from helper.messages import MSG
from helper.controller import BackendQueryController
from helper.controller import BackendSerializerController
from helper.constants import USER_REDIRECT_PATH
from helper.utils import json_dict_parser

from users.serializers import UserProfileSerializer


class UserProfileDetails:
    """
    UserProfileDetails
    This "UserProfileDetails" class module used to get, create, update all user profile related 
    data use diffrent methods
        create_profile_one
        create_profile_second
        create_profile_third
    """

    def __init__(self, **kwargs):
        self.auth_user_id = kwargs.get('auth_user_id', None)
        self.input_request_data = kwargs.get('input_request_data', None)
        self.auth_user_instance = None

    def user_profile_create_process(self, request_data, redirect_path):
        """
        user_profile_create_process
        This "user_profile_create_process" method common used for update 
        the user profile details step by steps
        """
        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': self.auth_user_id})
        self.auth_user_instance = _backend_controller_instance.get_query_instance()
        if not self.auth_user_instance:
            return json_dict_parser(
                MSG['AUTH_USER_NOT_FOUND'], {}, True)

        # update user profile query using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=UserProfile,
            filter_req_data={'auth_user_id': self.auth_user_instance.id},
            input_req_data=request_data)
        user_update_status = _backend_controller_instance.update_query_set()
        if not user_update_status:
            return json_dict_parser(MSG['PROFILE_NOT_UPDATE'], {}, False)
        return json_dict_parser(
            MSG['PROFILE_ONE_COMPLETED'],
            {'redirect_user_url': redirect_path},
            True)

    def create_profile_one(self):
        """
        create_profile_one
        profile one data passing with "user_profile_create_process" method
        talent, interest, price
        """
        return self.user_profile_create_process(
            {
                'is_first_step_completed': True,
                'talent': self.input_request_data.get('telent', None),
                'interest': self.input_request_data.get('interest', None),
                'price': self.input_request_data.get('price', None),
            }, USER_REDIRECT_PATH['SECOND']

        )

    def create_profile_second(self):
        """
        create_profile_second
        profile second data passing with "user_profile_create_process" method
        dob, city, gender, your_name
        """
        return self.user_profile_create_process(
            {
                'is_second_step_completed': True,
                'your_name': self.input_request_data.get('your_name', None),
                'dob': self.input_request_data.get('dob', None),
                'gender': self.input_request_data.get('gender', None),
                'country': self.input_request_data.get('country', None),
                'state': self.input_request_data.get('state', None),
                'city': self.input_request_data.get('city', None),
            }, USER_REDIRECT_PATH['THIRD']
        )

    def create_profile_third(self):
        """
        create_profile_third
        profile Third data passing with "user_profile_create_process" method
        profile_pic, short_intro
        """
        return self.user_profile_create_process(
            {
                'is_third_step_completed': True,
                'profile_picture': self.input_request_data.get('profile_picture', None),
                'short_intro': self.input_request_data.get('short_intro', None),
                'is_profile_completed': True,
            }, USER_REDIRECT_PATH['HOME']
        )

    def get_profile_details(self):
        """
        This "get_profile_details" methods used to get the profile details data
        """
        # user profile instance 
        # using userProfile models class
        _backend_controller_instance = BackendQueryController(
            model_name=UserProfile,
            filter_req_data={'auth_user_id': self.auth_user_id})
        user_profile_instance = _backend_controller_instance.get_query_instance()
        if not user_profile_instance:
            return json_dict_parser(MSG['DATA_NOT_FOUND'], {}, False)

        # backend serializer controller  
        # get the user profile serializer data using serializer class
        _backend_serializer_instance = BackendSerializerController(
            model_instance=user_profile_instance,
            type_serializer_data='__SINGLE__',
            serializer_class_name=UserProfileSerializer)
        serializer_data, message = _backend_serializer_instance.get_serializer_data()
        if not serializer_data:
            return json_dict_parser(message, {}, False)
        return json_dict_parser(
            message,
            serializer_data,
            True)
