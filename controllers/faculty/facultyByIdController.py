import django.http
from django.shortcuts import render
from django.http import response, request, JsonResponse, HttpResponse
from responses import sendResponse

def validateRequest(request,user_id):
    if not isinstance(user_id, str):
        response = sendResponse(None,f"Expected user_id to be of type int, got {type(user_id).__name__}",400)
        return response
    else:
        return None