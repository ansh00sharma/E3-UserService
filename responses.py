# API responses

from django.http import JsonResponse

def sendResponse(data=None,serverError=None, status=200):
    """
    Returns a standard JSON response format for API responses.

    Args:
        data (dict | None): The main data payload for the response.
        message (str): A message describing the result or any information.
        status (int): The HTTP status code.

    Returns:
        JsonResponse: JSON response in a structured format.
    """

    if data is not None and not isinstance(data, dict):
        raise TypeError(f"Expected data to be of type dict or None, got {type(data).__name__}")
    if not isinstance(status, int):
        raise TypeError(f"Expected status to be of type int, got {type(status).__name__}")
    
    response = {
        "data": data,
        "message": responses[status],
        "serverError" : serverError,
        "status":status
    }
    return response


responses={
    200: 'Success',
    400: 'Invalid input',
    405: 'Method Not Allowed',
    500: 'Internal Server Error'
}