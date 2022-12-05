from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
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
    """
        회원 리스트 호출
        ---
        # 내용
            - title : 영화제목
            - year : 영화 출시 년도
            - genre : 영화 장르
    """
    member_list = serializers.serialize('json', User.objects.filter(user_type=1).order_by('-id'), fields=('user_name'))
    member_json = json.loads(member_list)

    response = {}
    response["result"] = "false"
    response["error_code"] = "301"
    response["message"] = "잘못된 요청입니다."
    response["return_url"] = "/"
    response["data"] = member_json
    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

    # print(member_json[0]['fields'])
    # return HttpResponse(member_json, content_type="text/json-comment-filtered")

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
class detail(APIView):
    def get(self, request):
        member_detail = serializers.serialize('json', User.objects.filter(user_type=1).order_by('-id'), fields=('user_name', 'create_data', 'user_gender', 'user_height', 'user_weight'))
        return HttpResponse(member_detail, content_type="text/json-comment-filtered")

