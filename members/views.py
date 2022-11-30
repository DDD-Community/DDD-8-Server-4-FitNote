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

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def list(request):
    member_list = serializers.serialize('json', User.objects.filter(user_type=1).order_by('-id'), fields=('user_name'))
    return HttpResponse(member_list, content_type="text/json-comment-filtered")

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
class detail(APIView):
    def get(self, request):
        member_detail = serializers.serialize('json', User.objects.filter(user_type=1).order_by('-id'), fields=('user_name', 'create_data', 'user_gender', 'user_height', 'user_weight'))
        return HttpResponse(member_detail, content_type="text/json-comment-filtered")

