from rest_framework import status
from rest_framework.exceptions import APIException


class LineServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Line service not available"
    default_code = "line_service_unavailable"
