

import re


# Make a regular expression
# for validating an Email
REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def is_valid_mobile_number(mobile_number):
    """
    # 1) Begins with 0 or 91
    # 2) Then contains 7 or 8 or 9.
    # 3) Then contains 9 digits
    """
    pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return pattern.match(mobile_number)


def mobile_number_validate(mobile_number):
    """
    this "mobile_number_validate" function used to validate mobile number is valid or not
    """
    if (is_valid_mobile_number(mobile_number)):
        return True
    return False


def is_valid_email(email):
    """
    check email is valid or not as per post data
    """
    if(re.fullmatch(REGEX, email)):
        return True
    return False


def get_auth_service_type(username):
    """
    This Function used to get the service types of auth
    """
    try:
        if is_valid_mobile_number(username):
            return 'phone'
        return 'email'
    except Exception as e:
        print(e)
        return 'phone'


def json_dict_parser(message, data, status):
    """
    This "dict_parser" function used to parse 
    the all python module dict data with same format ways
    It has been used repeatedly to avoid the format of writing code.
    first: message
    second: data
    third: status
    """
    return dict(status=status,
                message=message,
                data=data)
