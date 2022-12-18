from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def docs(request):
    return render(request, 'docs.html')

@api_view(['GET'])
def memberDocs(request):
    return render(request, 'memberDocs.html')

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def getApi(request):
    posts = []
    post_list = serializers.serialize('json', posts)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")
