import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('api')
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code
    else:
        logger.exception(exc)
        response = Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data={
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'error_message': '서버 에러 입니다.',
                'error_details': repr(exc)
            },
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )

    return response
