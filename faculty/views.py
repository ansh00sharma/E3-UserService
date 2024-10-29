from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from swagger_api import *
from responses import *
from django.http import JsonResponse
from responses import sendResponse
from controllers.faculty import *
from services.faculty import *
from data.faculty import *
from utils import *

# Create your views here.

# def allFaculty(request):
#     if request.method == 'GET':
#         pass
#     else:
#         return JsonResponse(sendResponse(None,405))

# API 10
# @swagger_auto_schema(method='post')
@api_view(['POST'])
def facultyById(request,user_id):
    """
        Sample of Faculty user_id should be like : FACxxxx (7 AplhaNumeric Letters) Combination
    """

    try:
        if request.method == 'POST':
            # Validate the Request by passing to Controller Layer
            response = facultyByIdController.validateRequest(request,user_id)
            if response:
                return JsonResponse(response)
            else:
                # Applying Business Logic through Service Layer if Validation Passes.
                facultyByIdService.validateUserId(user_id)
                # Passing Request to Data Layer
                response = facultyByIdData.getFaculty(user_id)
                return JsonResponse(sendResponse(data=response),safe=False)
        else:
            return JsonResponse(sendResponse(None,405),safe=False)
        
    except ServiceError as e:
        return JsonResponse(sendResponse(data=None, serverError=e.message, status=e.status),safe=False)
    
    except DataDoesNotExist as e:
        return JsonResponse(sendResponse(data=None, serverError=e.message, status=e.status),safe=False)
    
    except Exception as e:
        return JsonResponse(sendResponse(data=None, serverError=str(e), status=500),safe=False)