from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        default_messages = {
            status.HTTP_400_BAD_REQUEST: {
                'detail': 'Bad Request',
                'code': 'bad_request',
                'message': 'Your request is invalid. Fix it now or face the consequences!'
            },
            status.HTTP_401_UNAUTHORIZED: {
                'detail': 'Unauthorized',
                'code': 'unauthorized',
                'message': 'Access denied! You dare trespass our forbidden realm? Retreat or prepare for obliteration!'
            },
            status.HTTP_403_FORBIDDEN: {
                'detail': 'Forbidden',
                'code': 'forbidden',
                'message': 'You have entered a forbidden zone. Turn back or face dire consequences!'
            },
            status.HTTP_404_NOT_FOUND: {
                'detail': 'Not Found',
                'code': 'not_found',
                'message': 'The resource you seek eludes your grasp. Abandon hope and accept your fate!'
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                'detail': 'Internal Server Error',
                'code': 'internal_server_error',
                'message': 'A catastrophic failure has occurred within our system. Brace yourself for the impending chaos!'
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