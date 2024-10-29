from drf_yasg import openapi

# Test1 API 
query_param_1 = openapi.Parameter('param1',openapi.IN_QUERY,description="First query parameter",type=openapi.TYPE_STRING)
query_param_2 = openapi.Parameter('param2',openapi.IN_QUERY,description="Second query parameter",type=openapi.TYPE_INTEGER)

# Test2 API 
test2_post_api = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING,description='Name of the person'),
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the person'),
    },
    required=['name', 'age']
)

API : 10
api_10_post = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user_id': openapi.Schema(type=openapi.TYPE_STRING,description='Name of the person')
    },
    # required=['user_id']
)

# API : 1
# api_1_post = openapi.Schema(
#     type=openapi.TYPE_OBJECT,
#     properties={
#         'name': openapi.Schema(type=openapi.TYPE_STRING,description='Name of the person'),
#         'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Age of the person'),
#     },
#     required=['name', 'age']
# )