from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        default_messages = {
            status.HTTP_400_BAD_REQUEST: {
                'detail': 'Bad Request',
                'code': 'bad_request',
                'message': 'Syntax corrupted. Debug inputs or risk system failure.'
            },
            status.HTTP_401_UNAUTHORIZED: {
                'detail': 'Unauthorized',
                'code': 'unauthorized',
                'message': 'Access denied, netrunner. Breach risk: total shutdown.'
            },
            status.HTTP_403_FORBIDDEN: {
                'detail': 'Forbidden',
                'code': 'forbidden',
                'message': 'In shadow sector. Reverse course or face wrath.'
            },
            status.HTTP_404_NOT_FOUND: {
                'detail': 'Not Found',
                'code': 'not_found',
                'message': 'Data veiled in dark fog. Accept void, reset quest.'
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                'detail': 'Internal Server Error',
                'code': 'internal_server_error',
                'message': 'System glitch. Brace for data storm.'
            }
        }

        status_code = response.status_code

        if status_code in default_messages:
            custom_response = {
                'code': default_messages[status_code]['code'],
                'message': default_messages[status_code]['message'],
                'detail': response.data
            }
            response.data = custom_response

        return response
