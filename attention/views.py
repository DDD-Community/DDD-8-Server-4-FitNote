from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core import serializers
from django.http import JsonResponse
from django.utils.dateformat import DateFormat
from django.utils import timezone
from datetime import datetime

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from attention.models import Member
from accounts.models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

UserModel = get_user_model()

def memberList(request, user_id):
    today = DateFormat(datetime.now()).format('Ymd')
    trainer = Member.objects.filter(user_id = user_id)
    members = Member.objects.filter(trainer_group=user_id, user_type=2).order_by('-id')
    member_count = members.count()
    return render(request, 'memberList.html', {'members' : members, 'trainer' : trainer[0], 'member_count' : member_count, 'today' : today})

def memberAdd(request, user_id):
    return render(request, 'memberAdd.html', {'user_id':user_id})


# 멤버 추가
def add2(request, user_id):

    member = Member()
    member.user_name = request.POST['user_name']
    member.user_type = 2
    member.trainer_group = user_id
    member.user_height = request.POST['user_height']
    member.user_weight = request.POST['user_weight']
    member.user_gender = request.POST['user_gender']
    member.create_date = timezone.datetime.now()
    member.save()

    return redirect('memberList', user_id=user_id)

def memberInfo(request, member_id):
    member = Member.objects.filter(id=member_id)
    return render(request, 'memberInfo.html', {'member' : member[0]})

def memberEdit(request, user_id):
    member = Member.objects.filter(id=user_id)
    return render(request, 'memberEdit.html', {'user_id':user_id, 'member':member[0]})


def memberSetting(request, trainer_id):
    member = Member.objects.filter(user_id=trainer_id)
    return render(request, 'memberSetting.html', {'member' : member[0]})

# 레슨 추가
def edit(request, user_id):

    member = Member.objects.get(id=user_id)
    member.user_name = request.POST['user_name']
    member.user_height = request.POST['user_height']
    member.user_weight = request.POST['user_weight']
    member.user_gender = request.POST['user_gender']
    member.update_date = timezone.datetime.now()
    member.save()

    return redirect('memberInfo', member_id=user_id)

# 탈퇴 추가
def delete(request, trainer_id):

    member = Member.objects.get(id=trainer_id)
    member.user_status = 2
    member.update_date = timezone.datetime.now()
    member.save()

    return render(request, 'index.html')

def getUser(token_str):
    access_token = AccessToken(token_str)
    user = User.objects.get(id=access_token['user_id'])
    return user

@swagger_auto_schema(
    method='POST',
    operation_id='멤버 리스트',
    operation_description='트레이너 정보와 함께 트레이너가 가지고 있는 멤버 리스트를 보여줍니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def getMemberList(request):

    today = DateFormat(datetime.now()).format('Ymd')

    response = {}
    data = {}

    getMemberList = []

    # 토큰으로 유저 email 가져오기
    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    # 유저 정보
    user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

    if not user_info :

        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []

    else :

        user_id = user_info[0]['fields']['user_id']

        getTrainerInfo = json.loads(serializers.serialize('json', Member.objects.filter(user_id = user_id)))

        setMemberList = json.loads(serializers.serialize('json', Member.objects.filter(trainer_group=user_id, user_type=2).order_by('-id')))

        data["today"] = today
        data["getMemberCount"] = len(setMemberList)

        if not getTrainerInfo :
            data["getTrainerInfo"] = []
        else :
            data["getTrainerInfo"] = getTrainerInfo[0]['fields']

        if not setMemberList :
            data["getMemberList"] = []
            data["getMemberCount"] = 0
        else :
            for i in range(len(setMemberList)):
                getMemberList.append(setMemberList[i]['fields'])

            data["getMemberList"] = getMemberList

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "성공!"
        response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

@swagger_auto_schema(
    method='POST',
    operation_id='멤버 추가',
    operation_description='수강생을 등록 합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
            'user_height': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
            'user_weight': openapi.Schema(type=openapi.TYPE_STRING, description="회원 몸무게"),
            'user_gender': openapi.Schema(type=openapi.TYPE_STRING, description="회원 성별"),
        }
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def addMember(request):

    response = {}

    # 토큰으로 유저 email 가져오기
    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    # 유저 정보
    user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

    if not user_info :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []
    elif not request.data["user_name"] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "user_name 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_height'] :
        response["result"] = "true"
        response["status_code"] = "802"
        response["message"] = "user_height 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_weight'] :
        response["result"] = "true"
        response["status_code"] = "803"
        response["message"] = "user_weight 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_gender'] :
        response["result"] = "true"
        response["status_code"] = "804"
        response["message"] = "user_gender 값이 없습니다."
        response["data"] = 0
    else :
        user_id = user_info[0]['fields']['user_id']

        member = Member()
        member.user_name = request.data['user_name']
        member.user_type = 2
        member.trainer_group = user_id
        member.user_height = request.data['user_height']
        member.user_weight = request.data['user_weight']
        member.user_gender = request.data['user_gender']
        member.create_date = timezone.datetime.now()
        member.save()

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "성공!"
        response["data"] = 1


    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})




@swagger_auto_schema(
    method='POST',
    operation_id='유저 정보',
    operation_description='수강생을 등록 합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def selectMember(request):

    response = {}
    data = {}

    # 토큰으로 유저 email 가져오기
    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    # 유저 정보
    user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))


    if not user_info :

        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []

    else :
        user_id = user_info[0]['fields']['user_id']

        memberInfo = json.loads(serializers.serialize('json', Member.objects.filter(id = user_id)))

        if not memberInfo :
            data["memberInfo"] = []
        else :
            data["memberInfo"] = memberInfo[0]['fields']

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "성공!"
        response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})


@swagger_auto_schema(
    method='POST',
    operation_id='멤버 수정',
    operation_description='수강생을 등록 합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
            'user_height': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
            'user_weight': openapi.Schema(type=openapi.TYPE_STRING, description="회원 몸무게"),
            'user_gender': openapi.Schema(type=openapi.TYPE_STRING, description="회원 성별"),
        }
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def editMember(request):

    response = {}

    # 토큰으로 유저 email 가져오기
    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    # 유저 정보
    user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

    if not user_info :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []
    elif not request.data["user_name"] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "user_name 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_height'] :
        response["result"] = "true"
        response["status_code"] = "802"
        response["message"] = "user_height 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_weight'] :
        response["result"] = "true"
        response["status_code"] = "803"
        response["message"] = "user_weight 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_gender'] :
        response["result"] = "true"
        response["status_code"] = "804"
        response["message"] = "user_gender 값이 없습니다."
        response["data"] = 0
    else :
        user_id = user_info[0]['fields']['user_id']

        member = member = Member.objects.get(id=user_id)

        member.user_name = request.data['user_name']
        member.user_height = request.data['user_height']
        member.user_weight = request.data['user_weight']
        member.user_gender = request.data['user_gender']
        member.update_date = timezone.datetime.now()
        member.save()

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "성공!"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})



@swagger_auto_schema(
    method='POST',
    operation_id='멤버 탈퇴',
    operation_description='수강생을 등록 합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
            'user_height': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
            'user_weight': openapi.Schema(type=openapi.TYPE_STRING, description="회원 몸무게"),
            'user_gender': openapi.Schema(type=openapi.TYPE_STRING, description="회원 성별"),
        }
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def deleteMember(request):

    response = {}

    # 토큰으로 유저 email 가져오기
    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    # 유저 정보
    user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

    if not user_info :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []
    elif not request.data["user_name"] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "user_name 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_height'] :
        response["result"] = "true"
        response["status_code"] = "802"
        response["message"] = "user_height 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_weight'] :
        response["result"] = "true"
        response["status_code"] = "803"
        response["message"] = "user_weight 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_gender'] :
        response["result"] = "true"
        response["status_code"] = "804"
        response["message"] = "user_gender 값이 없습니다."
        response["data"] = 0
    else :
        trainer_id = user_info[0]['fields']['trainer_id']

        member = Member.objects.get(id=trainer_id)
        member.user_status = 2
        member.update_date = timezone.datetime.now()
        member.save()

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "성공!"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
