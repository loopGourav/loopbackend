"""
all constants for user app
"""

from datetime import timedelta

# choices fields

USER_TYPE = (('customer', 'CUSTOMER'),)
LOGIN_USER_TYPE = (('native', 'Native'), ('google-oauth2', 'Google'))
DEVICE_TYPE = [
    ('ios', 'Mobile/IOS'),
    ('android', 'Mobile/ANDROID'),
    ('web', 'WEB')
]
SERVICE_TYPE = [('phone', 'Phone Number'), ('email', 'Email ID')]
OTP_STATUS = [
    ('delivered', 'Delivered'),
    ('not_delivered', 'Not Delivered'),
    ('successful', 'Successful'),
    ('expired', 'Expired')
]
REGISTRATION_SOURCE = [
    ('API', 'API'),
    ('TEMPLATE', 'TEMPLATE')
]

PAYMENT_STATUS = (('pending', 'Pending'), ('success','Success'), ('failed', 'Failed'))
VIDEO_CALL_STATUS = (('pending', 'Pending'), ('accept', 'Accept'),
                     ('is_active', 'Active'), ('decline', 'Decline'))

USER_REDIRECT_PATH = dict(
    HOME="/home/dashboard/",
    FIRST="/users/profile-one/",
    SECOND="/users/profile-second/",
    THIRD="/users/profile-third/",
    LOGOUT="/users/logout"
)

# sms and email expiry time out in minutes
SMS_OTP_EXPIRY = timedelta(minutes=30)
EMAIL_OTP_EXPIRY = timedelta(minutes=30)

