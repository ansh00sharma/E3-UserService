from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from swagger_api import *
from responses import *
from faculty.models import Faculty


# Test Api
@swagger_auto_schema(method='post',request_body=test2_post_api,responses=responses)
@swagger_auto_schema(method='get',manual_parameters=[query_param_1, query_param_2],responses=responses)
@api_view(['GET','POST'])
def test(request):
    """ Description : """
    if request.method == 'GET':
        
        return Response({'message':'test working successful'})
    else:
        records = {
        'name':'ANSH',
        'age': 40
        }
        Faculty.insert_one(records)
        return Response({'message':'test data added successful'})


# API : 1
# @swagger_auto_schema(method='get',responses=responses)
# @api_view(['GET'])
# def home(request):
#     return JsonResponse({'message':'successful'})