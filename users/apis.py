
from datetime import date
from datetime import datetime

# Rest Apps
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# module
from helper.api_response_parser import APIResponseParser
from helper.messages import WEB_ALERT_MESSAGES, API_RESPONSE_MSG
from users.user_modules.registration_login import RegistrationLoginModule
from users.user_modules.user_profile import UserProfileDetails
from users.user_modules.user_otp_generation import OTPVerification


class RegistrationLoginApi(LoggingMixin, APIView):
    """
    RegistrationLoginApi
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    path: /users/api/registration/login
    method: POST
    usage: This endpoint used to user login and registration process with email and phone number
    request_body:{
        "username": "9909209890/Gourav.sharma@gmail.com"
    }
    response: {
        "user_data": {
            "auth_user_id": "15",
            "is_new_user_status": false,
            "otp_sent_status": true
        },
        "message": "Old User login Success",
        "status": true,
        "errors": []
    }
    """

    def final_response(self, new_old_status, auth_user_id, otp_sent_status, message):
        """
        This "final_response" used to get common response for old and new user in api 
        with new user status
        """
        return APIResponseParser.response_with_status(
            status=True,
            message=message,
            errors=[],
            data={
                'user_data': {
                    'auth_user_id': str(auth_user_id),
                    'is_new_user_status': new_old_status,
                    'otp_sent_status': otp_sent_status
                }
            },
            status_code=status.HTTP_200_OK)

    def post(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        if not request.data.get('username', None):
            return APIResponseParser.response_with_status(
                status=False,
                message=WEB_ALERT_MESSAGES['USERNAME_NOT_ENTERED'],
                errors=[{'username': API_RESPONSE_MSG['USERNAME_FIELD_REQUIRED']}],
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)

        # Registration Login module
        # created at 21 august 2021 by Gourav Sharma (^_^)
        # separate login module for using all view
        _login_user_instance = RegistrationLoginModule(
            username=request.data['username'],
            source_type='API',
            device_type=request.data.get('device_type', 'android'))
        login_user_dict = _login_user_instance.registration_login_process()

        # final response according to all status logic
        # condition for manage web redirect path
        if login_user_dict['status'] is True:
            if login_user_dict['data']['is_new_user'] is True:
                return self.final_response(True,
                                           login_user_dict['data']['user_id'],
                                           login_user_dict['data']['otp_sent'],
                                           login_user_dict['message'])
            return self.final_response(
                False,
                login_user_dict['data']['user_id'],
                login_user_dict['data']['otp_sent'],
                login_user_dict['message'])

        # exception module error response
        return APIResponseParser.response_with_status(
            status=False,
            message=login_user_dict['message'],
            errors=[{'errors_message': login_user_dict['message']}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)


class OTPVerificationApi(LoggingMixin, APIView):
    """
    OTPVerificationApi
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    path: /users/api/otp/verification
    method: POST
    usage: This endpoint used to user verify the otp with our valid number and mail
    request_body:{
        "auth_user_id": "16",
        "OTP": "533181"
    }
    response: {
        "access_code": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
        eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMwMTQzNTYzLCJqdGkiOiI
        zYzMyOTYzOGE3ZWE0MDBkOWU0YmFkZjc0NGQxNjI2NiIsInVzZXJfaWQiOjE2fQ.
        eJ4GxzA-Zz_Nc3Fb0A58RYpxTs5i5IockWCPH5Pvn1Q",
        "is_otp_verified": false,
        "is_first_step_completed": false,
        "is_second_step_completed": false,
        "is_third_step_completed": false,
        "is_profile_completed": false,
        "message": "DONE",
        "status": true,
        "errors": []
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.errors = []

    def post(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        self.data = (
            request.query_params
            if len(request.data) == 0 else
            request.data.copy())
        if not self.data.get('OTP', None):
            self.errors.append(
                {'otp': API_RESPONSE_MSG['OTP_NOT_ENTERED']})
        if not self.data.get('auth_user_id', None):
            self.errors.append(
                {'auth_user_id': API_RESPONSE_MSG['AUTH_USER_REQUIRED']})

        if self.errors:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['REQUIRED'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)
        # OTP Module
        # for generate otp and send the sms and email
        otp_verification_instance = OTPVerification(
            auth_user_id=self.data.get('auth_user_id'),
            otp=self.data.get('OTP'),
            source_type='API')
        otp_status, otp_response_data, otp_message = otp_verification_instance()

        if otp_status:
            # Final Response with token data
            return APIResponseParser.response_with_status(
                status=True,
                message=otp_message,
                errors=[],
                data=otp_response_data,
                status_code=status.HTTP_200_OK)

        # otp module response manage with status and
        # response message data
        # negative case response with error message
        return APIResponseParser.response_with_status(
            status=False,
            message=otp_message,
            errors=[{'errors_message': otp_message}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)


class ProfileDetails(LoggingMixin, APIView):
    """
    ProfileDetails
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    Authrization: YES
    path: /users/api/profile/details
    method: GET
    usage: This endpoint used to get the user profile details
    response: {
    "user_profile_data": {
        "id": 13,
        "created_at": "2021-08-28T16:35:20.270137Z",
        "updated_at": "2021-08-28T16:35:20.270170Z",
        "is_active": true,
        "email": null,
        "isd": null,
        "phone_no": "9968047352",
        "profile_picture": "/Screenshot%20from%202021-08-17%2013-04-36.png",
        "short_intro": "gourav sharma is a coder",
        "price": 120.0,
        "talent": "Code",
        "interest": "reading",
        "your_name": "Gourav",
        "gender": "male",
        "dob": "1995-12-11",
        "device_type": null,
        "login_type": "native",
        "user_type": "customer",
        "device_id": null,
        "random_password_key": "9H00M5F10H",
        "is_otp_verified": false,
        "is_password_created": false,
        "is_first_step_completed": true,
        "is_second_step_completed": true,
        "is_third_step_completed": true,
        "is_profile_completed": true,
        "is_premium": false,
        "created_by": 17,
        "updated_by": null,
        "country": null,
        "state": null,
        "city": null,
        "auth_user": 17
    },
    "message": "DONE",
    "status": true,
    "errors": []
    }
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        if not request.user:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['TOKEN_NOT_VALID'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)

        # UserProfileDetails module
        # used for get user profile data
        _user_profile_instance = UserProfileDetails(
            auth_user_id=request.user.id)
        user_profile_dict = _user_profile_instance.get_profile_details()
        if user_profile_dict['status']:
            return APIResponseParser.response_with_status(
                status=True,
                message=user_profile_dict['message'],
                errors=[],
                status_code=status.HTTP_200_OK,
                data={
                    'user_profile_data': user_profile_dict['data']
                },
            )
        # otp module response manage with status and
        # response message data
        # negative case response with error message
        return APIResponseParser.response_with_status(
            status=False,
            message=user_profile_dict['message'],
            errors=[{'errors_message': user_profile_dict['message']}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)


class ProfileOneApi(LoggingMixin, APIView):
    """
    UserProfileOneApi
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    path: /users/api/profile/one
    method: POST
    usage: This endpoint used to user verify the otp with our valid number and mail
    Authorization: YES
    request_body:{
       "telent": "Code",
        "price": "120",
        "interest": "reading"
    }
    response: {
        "message": "Profile completed",
        "status": true,
        "errors": []
    }
    """

    permission_classes = (IsAuthenticated, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.errors = []

    def request_data_validation(self):
        """
        This "empty_data_key" method used to get empty type validation error 
        for profile one details
        """
        if not self.data.get('telent', None):
            self.errors.append(
                {'telent': API_RESPONSE_MSG['REQUIRED'].format('telent')})
        if not self.data.get('telent').isalpha():
            self.errors.append(
                {'telent': API_RESPONSE_MSG['STRING_WARNING']})
        if not self.data.get('price', None):
            self.errors.append(
                {'price': API_RESPONSE_MSG['REQUIRED'].format('price')})
        if not self.data.get('price'):
            self.errors.append(
                {'price': API_RESPONSE_MSG['NUMBER_WARNING']})
        if not self.data.get('interest', None):
            self.errors.append(
                {'interest': API_RESPONSE_MSG['REQUIRED'].format('interest')})
        if not self.data.get('interest').isalpha():
            self.errors.append(
                {'interest': API_RESPONSE_MSG['STRING_WARNING']})

    def post(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        if not request.user:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['TOKEN_NOT_VALID'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)
        self.data = (
            request.query_params
            if len(request.data) == 0 else
            request.data.copy())
        self.request_data_validation()
        if self.errors:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['REQUIRED_WARN'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)
        # UserProfileDetails module
        # used for create user profile first step
        _user_profile_instance = UserProfileDetails(
            input_request_data=self.data,
            auth_user_id=request.user.id)
        user_profile_dict = _user_profile_instance.create_profile_one()
        if user_profile_dict['status']:
            # Final Response with token data
            return APIResponseParser.response_with_status(
                status=True,
                message=user_profile_dict['message'],
                errors=[],
                data=user_profile_dict['data'],
                status_code=status.HTTP_200_OK)
        # otp module response manage with status and
        # response message data
        # negative case response with error message
        return APIResponseParser.response_with_status(
            status=False,
            message=user_profile_dict['message'],
            errors=[{'errors_message': user_profile_dict['message']}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)


class ProfileSecondApi(LoggingMixin, APIView):
    """
    UserProfileSecondApi
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    path: /users/api/profile/second
    method: POST
    Authorization: YES
    usage: This endpoint used to user verify the otp with our valid number and mail
    request_body:{
        "your_name": "Gourav",
        "dob": "1995-12-11",
        "gender": "male"
    }
    response: {
        "message": "Profile completed",
        "status": true,
        "errors": []
    }
    """

    permission_classes = (IsAuthenticated, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.errors = []

    @staticmethod
    def age_formula(birth_date):
        """
        calculate_age
        calculate the age of candidate(service provider)
        """
        return int((date.today() - birth_date).days / 365.2425)

    def calculate_candidate_age(self):
        """
        calculate_candidate_age
        This "calculate_candidate_age" method used to calculate 
        the candidate age according to user age
        """
        # age calculation value validation
        candidate_age = self.age_formula(datetime.strptime(
            self.data['dob'], '%Y-%m-%d').date())
        if candidate_age < 18 and 55 > candidate_age:
            self.errors.append({'dob': API_RESPONSE_MSG['CANDIDATE_AGE']})

    def request_data_validation(self):
        """
        This "empty_data_key" method used to get empty type validation error 
        for profile one details
        """
        if not self.data.get('your_name', None):
            self.errors.append(
                {'your_name': API_RESPONSE_MSG['REQUIRED'].format('your_name')})
        if not self.data.get('your_name').isalpha():
            self.errors.append(
                {'your_name': API_RESPONSE_MSG['STRING_WARNING']})
        if not self.data.get('dob', None):
            self.errors.append(
                {'dob': API_RESPONSE_MSG['DATETIME_VALID_REQUIRED'].format('dob')})
        if not self.data.get('gender', None):
            self.errors.append(
                {'gender': API_RESPONSE_MSG['REQUIRED'].format('gender')})
        if not self.data.get('gender').isalpha():
            self.errors.append(
                {'gender': API_RESPONSE_MSG['STRING_WARNING']})

    def post(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        if not request.user:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['TOKEN_NOT_VALID'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)

        self.data = (
            request.query_params
            if len(request.data) == 0 else
            request.data.copy())
        self.request_data_validation()
        self.calculate_candidate_age()
        if self.errors:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['REQUIRED'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)

        # UserProfileDetails module
        # used for create user profile second step
        _user_profile_instance = UserProfileDetails(
            input_request_data=self.data,
            auth_user_id=request.user.id)
        user_profile_dict = _user_profile_instance.create_profile_second()

        if user_profile_dict['status']:
            # Final Response with token data
            return APIResponseParser.response_with_status(
                status=True,
                message=user_profile_dict['message'],
                errors=[],
                data=user_profile_dict['data'],
                status_code=status.HTTP_200_OK)

        # otp module response manage with status and
        # response message data
        # negative case response with error message
        return APIResponseParser.response_with_status(
            status=False,
            message=user_profile_dict['message'],
            errors=[{'errors_message': user_profile_dict['message']}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)


class ProfileThirdApi(APIView):
    """
    UserProfileThirdApi
    creaated at 28 August 2021 by Gourav Sharma(^_^)
    path: /users/api/profile/third
    method: POST
    Authorization: YES
    usage: This endpoint used to user verify the otp with our valid number and mail
    request_body:
        short_intro: gourav sharma is a coder
        profile_picture: media-file
    response: {
        "message": "Profile completed",
        "status": true,
        "errors": []
    }
    """

    permission_classes = (IsAuthenticated, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = {}
        self.errors = []

    def post(self, request):
        """
        this post() methods used to post the registration and login usernmae according to
        user request from the client
        """
        if not request.user:
            return APIResponseParser.response_with_status(
                status=False,
                message=API_RESPONSE_MSG['TOKEN_NOT_VALID'],
                errors=self.errors,
                data={},
                status_code=status.HTTP_400_BAD_REQUEST)

        self.data = (
            request.query_params
            if len(request.data) == 0 else
            request.data.copy())

        # UserProfileDetails module
        # used for create user profile final step
        _user_profile_instance = UserProfileDetails(
            input_request_data=self.data,
            auth_user_id=request.user.id)
        user_profile_dict = _user_profile_instance.create_profile_third()

        if user_profile_dict['status']:
            # Final Response with token data
            return APIResponseParser.response_with_status(
                status=True,
                message=user_profile_dict['message'],
                errors=[],
                data=user_profile_dict['data'],
                status_code=status.HTTP_200_OK)

        # otp module response manage with status and
        # response message data
        # negative case response with error message
        return APIResponseParser.response_with_status(
            status=False,
            message=user_profile_dict['message'],
            errors=[{'errors_message': user_profile_dict['message']}],
            data={},
            status_code=status.HTTP_400_BAD_REQUEST)
