from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from accounts.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.views import APIView 
from django.http import JsonResponse

import json

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def list(request):
    member_list = serializers.serialize('json', User.objects.filter(user_type=1).order_by('-id'), fields=('user_name'))
    member_json = json.loads(member_list)

    response = {}
    response["status"] = "true"
    response["code"] = "200"
    response["message"] = "정상 요청"
    response["data"] = member_json
    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def detail(request):
    
    print('--------------------------------')
    print(request.META['HTTP_AUTHORIZATION'][7:])
    print('--------------------------------')
    print(TokenUser(request.META['HTTP_AUTHORIZATION'][7:]))
    print('--------------------------------')

    user_name = request.GET['userName']

    member_detail = serializers.serialize('json', User.objects.filter(user_type=1, user_name=user_name).order_by('-id'), fields=('user_name', 'create_data', 'user_gender', 'user_height', 'user_weight'))
    member_json = json.loads(member_detail)

    response = {}
    response["status"] = "true"
    response["code"] = "200"
    response["message"] = "정상 요청"
    response["data"] = member_json

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

