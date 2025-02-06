from buses.utils.getClientIp import get_client_ip
from django.utils.timezone import now
import requests

 
def log_user_action(request,user_id,action):

    try:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        # Call Flask Logging API
        log_data = {
            "user_id": str(user_id),  # Assuming user.id is UUID
            "action": action,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "time": now().strftime('%H:%M:%S'),
            "date": now().strftime('%d-%m-%Y'),
            "day": now().strftime('%A')
        }
        requests.post("http://localhost:5000/log/", json=log_data, timeout=3)
        return True
    
    except requests.exceptions.RequestException as e:
        # print(f"Logging API Error: {e}")  # Avoid breaking login flow
        return False

    

