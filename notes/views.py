from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from dj_rest_auth.views import UserDetailsView
import requests
import json
from django.http import JsonResponse


def index(request):
    return render(request, 'index.html')

def docs(request):
    return render(request, 'docs.html')

def memberDocs(request):
    return render(request, 'memberDocs.html')

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def getApi(request):
    return JsonResponse(send_api('GET'), safe=False)

def send_api(method):
    API_HOST = "http://127.0.0.1:8000/accounts/user/"
    url = API_HOST
    headers = {
        'Content-Type': 'application/json'
        , 'charset': 'UTF-8'
        , 'Accept': '*/*'
        , 'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc1MTc1NjA1LCJpYXQiOjE2NzMzNjEyMDUsImp0aSI6Ijg2NTI0YWVmMTI5YjQ2YjA5YTYzZTBiZWJkMjhlNTA1IiwidXNlcl9pZCI6M30.rtys6gWZ-RE9Lq3q4wZsmBIAm4L25FGrYOjdc-Q14_4'}
    
    try:
        if method == 'GET':
            response = requests.get(API_HOST, headers=headers)
            return response.json()
    except Exception as ex:
        print(ex)
  
