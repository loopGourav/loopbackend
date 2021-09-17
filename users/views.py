from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib import messages

from django.contrib.auth.models import User
from helper.controller import BackendQueryController

from helper.messages import WEB_ALERT_MESSAGES
from users.user_modules.registration_login import RegistrationLoginModule

from users.user_modules.user_otp_generation import MutualOTPSystem, OTPVerification
from users.user_modules.password_manager import UserPasswordManager
from users.user_modules.user_profile import UserProfileDetails


# Create your views here.


class RegistrationLoginUserView(TemplateView):
    """
    RegistrationLoginUserView
    methods: GET/POST
    Path: /user/sign-up
    usage: This RegistrationLoginUserView() TemplateView used to start the sign up 
    process for the users
    """
    template_name = 'web/registration.html'

    def get(self, request):
        """get
        This get() method used to get the user sign up template 
        page for start the sign up process
        """
        return render(request, self.template_name, {})

    def post(self, request):
        """post
        This post methods used to post the user registration data with our credentials and 
        google authentication data
        """
        if not request.POST.get('username', None):
            messages.success(
                request, WEB_ALERT_MESSAGES['USERNAME_NOT_ENTERED'])
            return redirect('/user/registration/')

        # Registration Login module
        # created at 21 august 2021 by Gourav Sharma (^_^)
        # separate login module for using all view
        _login_user_instance = RegistrationLoginModule(
            username=request.POST.get('username', None),
            source_type='WEB')
        login_user_dict = _login_user_instance.registration_login_process()

        # final response according to all status logic
        # condition for manage web redirect path
        if login_user_dict['status'] is True:
            if login_user_dict['data']['is_new_user'] is True:
                messages.success(request, login_user_dict['message'])
                return redirect(''.join(['/users/otp-verification/',
                                         str(login_user_dict['data']['user_id'])]))
            messages.success(request, login_user_dict['message'])
            return redirect(''.join([
                '/users/password-verification/', str(login_user_dict['data']['user_id'])]))
        messages.success(request, login_user_dict['message'])
        return redirect('/users/registration/')


class OTPVerificationView(TemplateView):
    """
    UserOTPVerification
    path: /user/otp                     
    Methods: GET/POST
    Usage: This UserOTPVerification() TemplateView used to verify the valid 
    user using OTP Number
    Keys Name:
        "OTP": "980937",
        "customer_user_id": "5"
    In this module also used the user_id for help the 
    user identification for login process
    """
    template_name = 'web/otp.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': auth_user_id})
        auth_user_instance = _backend_controller_instance.get_query_instance()
        return render(request, self.template_name, {
            'auth_user_id': auth_user_id,
            'user_account_detail': str(auth_user_instance.username)})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use OTPVerification() module for help the verification 
        for a valid user with otp details
        """
        auth_user_id if auth_user_id else request.POST.get(
            'auth_user_id', None)
        if not auth_user_id:
            messages.success(request, WEB_ALERT_MESSAGES['USER_NOT_DEFINED'])
            return redirect(''.join(['/user/registration/']))
        # OTP Module
        # for generate otp and send the sms and email
        otp_verification_instance = OTPVerification(
            auth_user_id=auth_user_id,
            otp=request.POST.get('OTP', None),
            source_type='WEB'
        )
        otp_status, otp_data, otp_message = otp_verification_instance()
        print(otp_data)
        if not otp_status:
            messages.success(request, otp_message)
            return redirect(''.join(['/users/otp-verification/', str(auth_user_id)]))
        messages.success(request, otp_message)
        return redirect(''.join(['/users/password-generation/', str(auth_user_id)]))


class PasswordGenerationView(TemplateView):
    """
    PasswordGenerationView
    path: /user/otp
    Methods: GET/POST
    Usage: This PasswordGenerationView() TemplateView used to verify the valid 
    user using OTP Number
    """
    template_name = 'web/password_generation.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        return render(request, self.template_name, {'auth_user_id': auth_user_id})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use UserPasswordManager() module for help the generate a user 
        """
        auth_user_id = auth_user_id if auth_user_id else request.POST.get(
            'auth_user_id', None)
        if not auth_user_id:
            messages.success(request, WEB_ALERT_MESSAGES['USER_NOT_DEFINED'])
            return redirect(''.join(['/users/registration/']))

        # UserPasswordManager module
        # used for generate the new user password to authenticate the new user
        _password_manager_instance = UserPasswordManager(
            request_instance=request,
            password=request.POST.get('password', None),
            confirm_password=request.POST.get('confirm_password', None),
            auth_user_id=auth_user_id,
            service_type='__REGISTRATION__')
        password_manager_dict = _password_manager_instance.password_generation()
        # Failed Status
        # error warning message retrun with alert
        if not password_manager_dict['status']:
            messages.success(request, password_manager_dict['message'])
            return redirect(''.join(['/users/password-generation/', str(auth_user_id)]))
        # Final Response For Verified User
        # To create Login password
        messages.success(request, password_manager_dict['message'])
        return redirect(''.join(['/users/profile-one/', str(auth_user_id)]))


class PasswordVerificationView(TemplateView):
    """
    UserOTPVerification
    path: /user/otp
    Methods: GET/POST
    Usage: This UserOTPVerification() TemplateView used to verify the valid 
    user using OTP Number
    """
    template_name = 'web/password_verification.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        # get auth user instance using "BackendQueryController"
        # with passing parameter filter data
        _backend_controller_instance = BackendQueryController(
            model_name=User,
            filter_req_data={'id': auth_user_id})
        auth_user_instance = _backend_controller_instance.get_query_instance()
        return render(request, self.template_name, {
            'user_id': auth_user_id,
            'user_account_detail': str(auth_user_instance.username)})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use UserPasswordManager() module for help the verification the password
        for a valid user with authentication instance
            # UserPasswordManager module
            # used for authenticate and verification authenticate the old user  
        """
        _password_manager_instance = UserPasswordManager(
            request_instance=request,
            password=request.POST.get('password', None),
            auth_user_id=auth_user_id if auth_user_id else request.POST.get(
                'auth_user_id', None))
        password_manager_dict = _password_manager_instance.password_verification()

        # Failed Status
        # error warning message retrun with alert
        if not password_manager_dict['status']:
            messages.success(request, password_manager_dict['message'])
            return redirect(''.join(['/users/password-verification/', str(auth_user_id)]))

        # Final Response For Verified User
        # To create Login password
        messages.success(request, password_manager_dict['message'])
        return redirect(''.join([
            password_manager_dict['data']['redirect_user_url'],
            str(auth_user_id)]))


class ProfileOneView(TemplateView):
    """
    ProfileOneView
    path: /user/otp
    Methods: GET/POST
    Usage: This ProfileOneView() TemplateView used to create one profile
    """
    template_name = 'web/profile_one.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        return render(request, self.template_name, {'auth_user_id': auth_user_id})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use UserProfileDetails() module for help the create user profile first step
        """
        auth_user_id = auth_user_id if request.user is None else request.user.id
        if auth_user_id:
            # UserProfileDetails module
            # used for create user profile first step
            _user_profile_instance = UserProfileDetails(
                input_request_data=request.POST,
                auth_user_id=auth_user_id)
            user_profile_dict = _user_profile_instance.create_profile_one()
            # manage status with accroding module response
            if not user_profile_dict['status']:
                messages.success(request, user_profile_dict['message'])
                return redirect(''.join(['/user/password-verification/', str(auth_user_id)]))
            messages.success(request, user_profile_dict['message'])
            return redirect(''.join([user_profile_dict['data']['redirect_user_url'], str(auth_user_id)]))
        # auth user not found
        messages.success(request, WEB_ALERT_MESSAGES['USER_NOT_DEFINED'])
        return redirect(''.join(['/user/registration/']))


class ProfileSecondView(TemplateView):
    """
    ProfileSecondView
    path: /user/otp
    Methods: GET/POST
    Usage: This ProfileSecondView() TemplateView used to create second profile
    """
    template_name = 'web/profile_second.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        return render(request, self.template_name, {'auth_user_id': auth_user_id})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use UserProfileDetails() module for help the create user profile second step
        """
        auth_user_id = auth_user_id if request.user is None else request.user.id
        if auth_user_id:
            # UserProfileDetails module
            # used for create user profile second step
            _user_profile_instance = UserProfileDetails(
                input_request_data=request.POST,
                auth_user_id=auth_user_id)
            user_profile_dict = _user_profile_instance.create_profile_second()
            # manage status with accroding module response
            if not user_profile_dict['status']:
                messages.success(request, user_profile_dict['message'])
                return redirect(''.join(['/user/password-verification/', str(auth_user_id)]))
            messages.success(request, user_profile_dict['message'])
            return redirect(''.join([user_profile_dict['data']['redirect_user_url'], str(auth_user_id)]))
        # auth user not found
        messages.success(request, WEB_ALERT_MESSAGES['USER_NOT_DEFINED'])
        return redirect(''.join(['/user/registration/']))


class ProfileThirdView(TemplateView):
    """
    ProfileThirdView
    path: /user/otp
    Methods: GET/POST
    Usage: This ProfileThirdView() ewSD used to create one profile
    """
    template_name = 'web/profile_third.html'

    def get(self, request, auth_user_id):
        """get
        This get() methods used to get the otp verification page with using user 
        login id to help for verifing the user
        """
        return render(request, self.template_name, {'auth_user_id': auth_user_id})

    def post(self, request, auth_user_id):
        """post
        This post() method used to post the otp details for verified 
        the sign up user data and forgot user details
        In this method we use UserProfileDetails() module for help the create user profile final step
        """
        auth_user_id = auth_user_id if request.user is None else request.user.id
        if auth_user_id:
            # UserProfileDetails module
            # used for create user profile final step
            _user_profile_instance = UserProfileDetails(
                input_request_data=request.POST,
                auth_user_id=auth_user_id)
            user_profile_dict = _user_profile_instance.create_profile_third()
            # manage status with accroding module response
            if not user_profile_dict['status']:
                messages.success(request, user_profile_dict['message'])
                return redirect(''.join(['/user/password-verification/', str(auth_user_id)]))
            messages.success(request, user_profile_dict['message'])
            return redirect(''.join([user_profile_dict['data']['redirect_user_url'], str(auth_user_id)]))
        # auth user not found
        messages.success(request, WEB_ALERT_MESSAGES['USER_NOT_DEFINED'])
        return redirect(''.join(['/user/registration/']))
