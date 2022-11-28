from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import User

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def list(request):
    members = User.objects.filter(user_type=1).order_by('-create_date')
    member_list = serializers.serialize('json', members)
    return HttpResponse(member_list, content_type="text/json-comment-filtered")
