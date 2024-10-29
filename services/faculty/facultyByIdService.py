from responses import sendResponse
from utils.serviceErrorHandler import ServiceError

def validateUserId(user_id):
    if not user_id.startswith("FAC"):
        raise ServiceError(f"Expected user_id to start with 'FAC' but instead got {user_id[:3]}",400)
        
    if not len(user_id) == 7:
        raise ServiceError(f"Expected user_id to be of length 7 but instead got {len(user_id)}",400)
        
    else:
        return None