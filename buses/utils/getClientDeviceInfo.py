def get_client_device_info(request):
    """Extract device info from the User-Agent header"""
    return request.META.get('HTTP_USER_AGENT', 'Unknown Device')