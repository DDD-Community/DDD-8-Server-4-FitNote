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

## jwt 생성 : membership 테이블 적재 동시 수행하기 위한 함수
def jwt_signup(id, fullname, email):

    member = Member()
    member.user_id = id
    member.user_name = fullname
    member.user_email = email
    member.user_type = 1
    member.create_date = timezone.datetime.now()
    member.save()

    return 1

def getUser(token_str):
    access_token = AccessToken(token_str)
    user = User.objects.get(id=access_token['user_id'])
    return user

######################################################### 회원 목록 호출 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='회원 목록',
    operation_description=
        '로그인 되어있는 트레이너 정보와 함께 트레이너가 보유하고 있는 회원을 보여줍니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2516&t=Im3MqwNXHYe7aFjP-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getTrainerInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점"),
                'getMemberCount': openapi.Schema(type=openapi.TYPE_INTEGER, description="트레이너가 보유하고 있는 회원 수"),
                'getMemberList': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def getMemberList(request):

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

        getTrainerInfo = json.loads(serializers.serialize('json', Member.objects.filter(user_id=user_id)))
        setMemberList = json.loads(serializers.serialize('json', Member.objects.filter(trainer_group=user_id, user_type=2).order_by('-id')))

        if not getTrainerInfo :
            data["getTrainerInfo"] = []
        else :
            data["getTrainerInfo"] = getTrainerInfo[0]['fields']

        data["getMemberCount"] = len(setMemberList)

        if not setMemberList :
            data["getMemberList"] = []
            data["getMemberCount"] = 0
        else :
            for i in range(len(setMemberList)):
                # pk 강제 삽입
                setMemberList[i]['fields']['id'] = Member.objects.filter(trainer_group=user_id, user_type=2).values_list('id', flat=True).order_by('-id')[i]
                getMemberList.append(setMemberList[i]['fields'])
                
            data["getMemberList"] = getMemberList

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원 목록 호출 END #########################################################

######################################################### 회원 추가 호출 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='회원 추가',
    operation_description=
            '트레이너가 관리하는 회원을 추가합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=162%3A2522&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_name': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
            'user_height': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키"),
            'user_weight': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 몸무게"),
            'user_gender': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 성별"),
        }
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 8xx: 실패"),
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
        response["message"] = "success"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원 추가 호출 END #########################################################

######################################################### 회원 상세 정보 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='회원 상세 정보',
    operation_description=
        '트레이너가 관리하는 회원의 상세정보를 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=107%3A4747&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberList': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, id : 추가 된 회원의 pk"),
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

        getMemberList = json.loads(serializers.serialize('json', Member.objects.filter(user_id=user_id)))

        if not getMemberList :
            data["getMemberList"] = []
        else :
            data["getMemberList"] = getMemberList[0]['fields']

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원 상세 정보 END #########################################################

######################################################### 회원 정보 수정 START #########################################################
@swagger_auto_schema(
    method='PUT',
    operation_id='회원 정보 수정',
    operation_description=
            '트레이너가 관리하는 회원의 정보를 수정합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=107%3A4935&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 Id"),
            'user_name': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 이름"),
            'user_height': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키"),
            'user_weight': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 몸무게"),
            'user_gender': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 성별"),
        }
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 8xx: 실패"),
            }
        )
    )}
)
@api_view(['PUT'])
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
    elif not request.data['user_name'] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "user_name 값이 없습니다."
        response["data"] = 0
    elif not request.data['user_gender'] :
        response["result"] = "true"
        response["status_code"] = "804"
        response["message"] = "user_gender 값이 없습니다."
        response["data"] = 0
    else :
        member = member = Member.objects.get(id=request.data['id'])

        member.user_name = request.data['user_name']
        member.user_height = request.data['user_height']
        member.user_weight = request.data['user_weight']
        member.user_gender = request.data['user_gender']
        member.update_date = timezone.datetime.now()
        member.save()

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원 정보 수정 END #########################################################

######################################################### 트레이너 회원 탈퇴 START #########################################################
@swagger_auto_schema(
    method='DELETE',
    operation_id='트레이너 회원 탈퇴',
    operation_description=
            '트레이너를 탈퇴 처리 합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=162%3A2608&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
    ),
    tags=['attention'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 8xx: 실패"),
            }
        )
    )}
)
@api_view(['DELETE'])
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
    else :
        trainer_id = user_info[0]['pk']

        member = Member.objects.get(id=trainer_id)
        member.user_status = 2
        member.update_date = timezone.datetime.now()
        member.save()

        user = UserModel.objects.get(id=trainer_id)
        user.delete()

        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
