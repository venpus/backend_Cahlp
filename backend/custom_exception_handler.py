# custom_exception_handler.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # Check if the exception is related to authentication
        if 'authentication credentials' in str(response.data):
            # Customize the response for authentication failures
            response.data = {
                'error': 'Authentication failed. Please provide valid credentials.'
            }
            response.status_code = status.HTTP_401_UNAUTHORIZED

    return response
