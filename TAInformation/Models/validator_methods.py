from TAInformation.Models.base_user import BaseUser
from curses.ascii import isupper, islower, isdigit
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Data validating methods module
# For all methods:
# Pre: Argument passed is derived from BaseUser
# Post: Returns dict object that indicates result of validation and error message, if needed


def id_validator(new_user: BaseUser):
    if new_user.user_id is None or new_user.user_id < 0:
        return {'result': False, 'errorMsg': "Invalid user id name entered\n"}

    return {'result': True, 'errorMsg': ""}


def name_validator(new_user: BaseUser):
    if new_user.name is None or len(new_user.name) < 5:
        return {'result': False, 'errorMsg': "Invalid name given\n"}

    return {'result': True, 'errorMsg': ""}


def password_validator(new_user: BaseUser):
    if new_user.password is None or len(new_user.password) < 4:
        return {'result': True, 'errorMsg': "Password must be at least 4 characters long\n"}

    uppercase_missing = True
    lowercase_missing = True
    number_missing = True
    special_char_missing = True

    # Loop to check if password format is correct
    for c in new_user.password:
        if isupper(c):
            uppercase_missing = False
        elif islower(c):
            lowercase_missing = False
        elif isdigit(c):
            number_missing = False
        else:
            special_char_missing = False

    error_msg = ""
    if uppercase_missing:
        error_msg += "Password must contain >= 1 uppercase letter\n"

    if lowercase_missing:
        error_msg += "Password must contain >= 1 lowercase letter\n"

    if number_missing:
        error_msg += "Password must contain >= 1 number\n"

    if special_char_missing:
        error_msg += "Password must contain >= 1 non-alphanumeric character\n"

    if error_msg != "":
        return {'result': False, 'errorMsg': error_msg}

    return {'result': True, 'errorMsg': ""}


def email_validator(new_user: BaseUser):
    try:
        validate_email(new_user.email)
    except ValidationError as errorMsg:
        return {'result': False, 'errorMsg': errorMsg}

    return {'result': True, 'errorMsg': ""}


def address_validator(new_user: BaseUser):
    if new_user.home_address is None:
        return {'result': False, 'errorMsg': "Home address is missing"}

    address_no_whitespace: str = new_user.home_address.replace(" ", "")
    if address_no_whitespace == "":
        return {'result': False, 'errorMsg': "Home address must contain some non-space characters"}

    return {'result': True, 'errorMsg': ""}


def phone_validator(new_user: BaseUser):
    if new_user.phone_number is None:
        return {'result': False, 'errorMsg': "No phone number given"}
    if len(new_user.phone_number) is not 13:
        return {'result': False, 'errorMsg': "Phone number should have exactly 13 characters"}

    char_set = {0, 4, 8}
    digit_set = set(range(13)) - char_set

    for index in range(13):
        if index in digit_set and not isdigit(new_user.phone_number.index(index)):
            return {'result': False, 'errorMsg': "Misplaced character in phone number entry"}

        if index == 0 and new_user.phone_number.index(0) != '(':
            return {'result': False, 'errorMsg': "Missing lead parentheses in phone number entry"}

        if index == 4 and new_user.phone_number.index(4) != '(':
            return {'result': False, 'errorMsg': "Missing trailing parentheses in phone number entry"}

        if index == 8 and new_user.phone_number.index(8) != '-':
            return {'result': False, 'errorMsg': "Missing dash between prefix and suffix in phone number entry"}

    return {'result': True, 'errorMsg': ""}

