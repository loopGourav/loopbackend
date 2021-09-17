from django.urls import path

from users.apis import RegistrationLoginApi
from users.apis import OTPVerificationApi
from users.apis import ProfileDetails
from users.apis import ProfileOneApi
from users.apis import ProfileSecondApi
from users.apis import ProfileThirdApi

from users.views import PasswordGenerationView
from users.views import ProfileOneView
from users.views import ProfileSecondView
from users.views import ProfileThirdView
from users.views import RegistrationLoginUserView
from users.views import OTPVerificationView
from users.views import PasswordVerificationView

urlpatterns = [
    path('registration/',
         RegistrationLoginUserView.as_view(),
         name='user_registration'),
    path('otp-verification/<str:auth_user_id>',
         OTPVerificationView.as_view(),
         name='user_otp_verification'),
    path('password-verification/<str:auth_user_id>',
         PasswordVerificationView.as_view(),
         name='user_password_verification'),
    path('password-generation/<str:auth_user_id>',
         PasswordGenerationView.as_view(),
         name='user_password_generation'),
    path('profile-one/<str:auth_user_id>',
         ProfileOneView.as_view(), name='user_profile_one'),
    path('profile-second/<str:auth_user_id>',
         ProfileSecondView.as_view(), name='user_profile_second'),
    path('profile-third/<str:auth_user_id>',
         ProfileThirdView.as_view(), name='user_profile_third'),
]

apis_urls = [
    path('api/registration/login', RegistrationLoginApi.as_view(),
         name='registration_login_api'),
    path('api/otp/verification', OTPVerificationApi.as_view(),
         name='otp_verification'),
    path('api/profile/details', ProfileDetails.as_view(), name='profile_details'),
    path('api/profile/first', ProfileOneApi.as_view(), name='profile_one'),
    path('api/profile/second', ProfileSecondApi.as_view(), name='profile_second'),
    path('api/profile/third', ProfileThirdApi.as_view(), name='profile_third'),

]

urlpatterns += apis_urls
