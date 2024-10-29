from faculty.models import Faculty
from responses import sendResponse
from utils.dataDoesNotExistHandler import *
from serializers.faculty import *


def getFaculty(user_id):
    record = Faculty.find_one({"user_id":user_id})
    if record:
        serialized_record = FacultySerializer(record).data
        return serialized_record
    
    else:
        raise DataDoesNotExist(f"Faculty with user_id {user_id} doesn't exist")