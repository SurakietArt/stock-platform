from rest_framework import status
from rest_framework.exceptions import APIException


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid token"
    default_code = "invalid_token"


class AuthUserNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found"
    default_code = "user_not_found"
