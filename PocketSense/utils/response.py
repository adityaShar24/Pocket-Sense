from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from functools import wraps


def response_any(status_code, status_message, data=None, error=None):
    res = {"status_code": status_code,
           "status_message": status_message}
    if data:
        res['data'] = data
    if error:
        res['error'] = error
    return Response(res, status=status_code)


def response_200(status_message, data=None):
    return Response({"status_code": HTTP_200_OK,
                     "status_message": status_message,
                     "data": data},
                    status=HTTP_200_OK)


def response_400_invalid_params(error):
    return Response({"status_code": HTTP_400_BAD_REQUEST,
                     "status_message": "Invalid query params",
                     "error": error},
                    status=HTTP_400_BAD_REQUEST)


def response_400_bad_request(status_message):
    return Response({"status_code": HTTP_400_BAD_REQUEST,
                     "status_message": status_message},
                    status=HTTP_400_BAD_REQUEST)


def response_validation_error(e):
    error_detail = e.detail
    error = None
    if isinstance(error_detail, dict):
        error = " | ".join([f"{k}: {v[0]}" for k, v in error_detail.items()])
    elif isinstance(error_detail, list):
        error = error_detail[0]
    return response_400_bad_request(error or error_detail)


def is_staff_user(input_func):
    """ User Staff Validator Decorator """

    @wraps(input_func)
    def decorator(request, *args, **kwargs):
        if not request.request.user.is_staff:
            return Response({"status_code": HTTP_401_UNAUTHORIZED,
                             "status_message": 'Unauthorized'},
                            status=HTTP_401_UNAUTHORIZED)

        return input_func(request, *args, **kwargs)

    return decorator
