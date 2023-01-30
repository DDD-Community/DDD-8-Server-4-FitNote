from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import JsonResponse
from django.core import serializers

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from hypeboy.models import Lesson
from attention.views import getUser
from attention.models import Member

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.utils.dateformat import DateFormat
from django.utils import timezone
from datetime import datetime

try:
    from django.utils import simplejson as json
except ImportError:
    import json

# Create your views here.
def hypeboy(request):
    return render(request, 'hypeboy.html')

def lessonAdd(request, user_id):
    today = DateFormat(datetime.now()).format('Ymd')
    member = Member.objects.filter(id=user_id)
    return render(request, 'lessonAdd.html', {'member' : member[0], 'today' : today})

def lessonIng(request, user_id):
    today = DateFormat(datetime.now()).format('Ymd')
    member = Member.objects.filter(id=user_id)
    lessons = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))

    if lessons :
        lessons_name_list = Lesson.objects.filter(user_id=user_id, start_date=lessons[0]['start_date'], view_yn=1).values('name').annotate(entries=Count('name'))
    else :
        lessons_name_list = []
        
    return render(request, 'lessonIng.html', {'member': member[0], 'lessons' : lessons, 'today' : today, 'lessons_name_list' : lessons_name_list})

def lessonNow(request, user_id, today):
    member = Member.objects.filter(id=user_id)
    lessons = Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1).order_by('completion', '-id', '-create_date')
    return render(request, 'lessonNow.html', {'lessons': lessons, 'user_id' : user_id, 'member' : member[0]})

def lessonEnd(request):
    return render(request, 'lessonEnd.html')

# 레슨 추가
def add(request, user_id, today):

    for i in range(1, int(request.GET['set'])+1) :
        lesson = Lesson()
        lesson.user_id = user_id
        lesson.name = request.GET['name']
        lesson.weight = request.GET['weight']
        lesson.count = request.GET['count']
        lesson.set = i
        lesson.start_date = today
        lesson.create_date = timezone.datetime.now()
        lesson.save()

    return redirect('lessonIng', user_id=user_id)

# 운동 미노출 처리
def delete(request, user_id, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)
    lessons.view_yn = 0
    lessons.save()
    
    return redirect('lessonNow', user_id=user_id, today=today)

# 운동 완료 처리
def completion(request, user_id, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)

    lessons.completion = 1
    lessons.save()
    
    return redirect('lessonNow', user_id=user_id, today=today)


def schedule(request):

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

        lessons_list = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))

        print(lessons_list)

        data["user_info"] = user_info[0]['fields']

        if not lessons_list :
            data["lessons_list"] = []
            data["exercise_list"] = []
        else :
            data["lessons_list"] = lessons_list[0]
            exercise_list = Lesson.objects.filter(user_id=user_info[0]['fields']['user_id'], start_date=lessons_list[0]['start_date'], view_yn=1).values('name').annotate(entries=Count('name'))

            if not exercise_list :
                data["exercise_list"] = []
            else :
                data["exercise_list"] = exercise_list

            response["result"] = "true"
            response["status_code"] = "200"
            response["message"] = "success"
            response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})


######################################################### 회원의 예정된 수업 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='예정된 수업',
    operation_description=
        '트레이너가 회원의 예정된 수업을 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=294%3A5057&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
                'lessons': openapi.Schema(type=openapi.TYPE_OBJECT, description="lessons_date : 수업 시작 날짜, \n lessons_name : 수업 운동 이름"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def ingLesson(request):

    response = {}
    data = {}

    if not request.data :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "id 값이 없습니다."
        response["data"] = []

        return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

    getMemberInfo = json.loads(serializers.serialize('json', Member.objects.filter(id=request.data['id'])))

    if not getMemberInfo :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []

    else :
        if getMemberInfo[0]['fields']['user_type'] == 1 :

            response["result"] = "true"
            response["status_code"] = "700"
            response["message"] = "트레이너 회원 입니다."
            response["data"] = []
        else :

            getMemberInfo[0]['fields']['id'] = Member.objects.filter(id=request.data['id'], user_type=2).values_list('id', flat=True).order_by('-id')[0]

            data["getMemberInfo"] = getMemberInfo[0]['fields']

            lessons_list = Lesson.objects.filter(user_id=request.data['id']).values('start_date').annotate(entries=Count('start_date'))

            if not lessons_list :
                data["lessons_list"] = []
                data["exercise_list"] = []
            else :

                data['lessons'] = []

                setName = []
                for i in range(0, int(len(lessons_list))) :

                    date = lessons_list[i]['start_date']
                
                    name = list(Lesson.objects.filter(user_id=request.data['id'], start_date=lessons_list[i]['start_date'], view_yn=1, total_completion=0).values('name').annotate(entries=Count('name')))

                    for j in range(0, int(len(name))):
                        setName.append(name[j]['name'])

                    data['lessons'].append({
                        "lessons_date": date,
                        "lessons_name": setName,
                    })

                    setName = []


                response["result"] = "true"
                response["status_code"] = "200"
                response["message"] = "success"
                response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 END #########################################################

######################################################### 회원의 예정된 수업 추가 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='회원 수업 추가',
    operation_description=
        '회원의 수업을 추가합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2770&t=9sYn60yjGqRDPLux-4',
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
                'getMemberList': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def addLesson(request):

    today = DateFormat(datetime.now()).format('Ymd')

    response = {}

    if not request.data :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "id 값이 없습니다."
        response["data"] = []

        return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

    getMemberInfo = json.loads(serializers.serialize('json', Member.objects.filter(id=request.data['id'])))

    if not getMemberInfo :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []
    else :
        if getMemberInfo[0]['fields']['user_type'] == 1 :

            response["result"] = "true"
            response["status_code"] = "700"
            response["message"] = "트레이너 회원 입니다."
            response["data"] = []
        else :
            if not request.data["set"] :
                response["result"] = "true"
                response["status_code"] = "801"
                response["message"] = "set 값이 없습니다."
                response["data"] = 0
            elif not request.data['name'] :
                response["result"] = "true"
                response["status_code"] = "802"
                response["message"] = "name 값이 없습니다."
                response["data"] = 0
            elif not request.data['weight'] :
                response["result"] = "true"
                response["status_code"] = "803"
                response["message"] = "weight 값이 없습니다."
                response["data"] = 0
            elif not request.data['count'] :
                response["result"] = "true"
                response["status_code"] = "804"
                response["message"] = "count 값이 없습니다."
                response["data"] = 0
            else :
                for i in range(1, int(request.data['set'])+1) :
                    lesson = Lesson()
                    lesson.user_id = request.data['id']
                    lesson.name = request.data['name']
                    lesson.weight = request.data['weight']
                    lesson.count = request.data['count']
                    lesson.set = i
                    lesson.start_date = today
                    lesson.create_date = timezone.datetime.now()
                    lesson.save()

                response["result"] = "true"
                response["status_code"] = "200"
                response["message"] = "success"
                response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 추가 END #########################################################


@swagger_auto_schema(
    method='POST',
    operation_id='레슨 제거',
    operation_description='수강생을 등록 합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lesson_id': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
        }
    ),
    tags=['hypeboy'],
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
def deleteLesson(request):

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
    elif not request.data["lesson_id"] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "lesson_id 값이 없습니다."
        response["data"] = 0
    else :
        user_id = user_info[0]['fields']['user_id']

        today = DateFormat(datetime.now()).format('Ymd')

        lessons = Lesson.objects.get(id=request.data['lesson_id'])
        lessons.view_yn = 0
        lessons.save()
        
        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = 1


    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})







######################################################### 회원의 종료된 수업 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='종료된 수업',
    operation_description=
        '트레이너가 회원의 종료된 수업을 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2672&t=2etd924LSzcLvhk6-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
                'lessons': openapi.Schema(type=openapi.TYPE_OBJECT, description="lessons_date : 수업 시작 날짜, \n lessons_name : 수업 운동 이름"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def endLesson(request):

    response = {}
    data = {}

    if not request.data :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "id 값이 없습니다."
        response["data"] = []

        return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

    getMemberInfo = json.loads(serializers.serialize('json', Member.objects.filter(id=request.data['id'])))

    if not getMemberInfo :
        response["result"] = "true"
        response["status_code"] = "800"
        response["message"] = "유저 정보 없음"
        response["data"] = []

    else :
        if getMemberInfo[0]['fields']['user_type'] == 1 :

            response["result"] = "true"
            response["status_code"] = "700"
            response["message"] = "트레이너 회원 입니다."
            response["data"] = []
        else :

            getMemberInfo[0]['fields']['id'] = Member.objects.filter(id=request.data['id'], user_type=2).values_list('id', flat=True).order_by('-id')[0]

            data["getMemberInfo"] = getMemberInfo[0]['fields']

            lessons_list = Lesson.objects.filter(user_id=request.data['id']).values('start_date').annotate(entries=Count('start_date'))

            if not lessons_list :
                data["lessons_list"] = []
                data["exercise_list"] = []
            else :

                data['lessons'] = []

                setName = []
                for i in range(0, int(len(lessons_list))) :

                    date = lessons_list[i]['start_date']
                
                    name = list(Lesson.objects.filter(user_id=request.data['id'], start_date=lessons_list[i]['start_date'], view_yn=1, total_completion=1).values('name').annotate(entries=Count('name')))

                    for j in range(0, int(len(name))):
                        setName.append(name[j]['name'])

                    data['lessons'].append({
                        "lessons_date": date,
                        "lessons_name": setName,
                    })

                    setName = []


                response["result"] = "true"
                response["status_code"] = "200"
                response["message"] = "success"
                response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 END #########################################################


# @swagger_auto_schema(
#     method='POST',
#     operation_id='운동 완료',
#     operation_description='수강생을 등록 합니다.',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'lesson_id': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
#         }
#     ),
#     tags=['hypeboy'],
#     responses={200: openapi.Response(
#         description="200 OK",
#         schema=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
#                 'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
#             }
#         )
#     )}
# )
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JWTAuthentication,))
# def sucLesson(request):

#     response = {}

#     # 토큰으로 유저 email 가져오기
#     email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

#     # 유저 정보
#     user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

#     if not user_info :
#         response["result"] = "true"
#         response["status_code"] = "800"
#         response["message"] = "유저 정보 없음"
#         response["data"] = []
#     elif not request.data["lesson_id"] :
#         response["result"] = "true"
#         response["status_code"] = "801"
#         response["message"] = "lesson_id 값이 없습니다."
#         response["data"] = 0
#     else :
#         user_id = user_info[0]['fields']['user_id']

#         today = DateFormat(datetime.now()).format('Ymd')

#         lessons = Lesson.objects.get(id=request.data['lesson_id'])
#         lessons.completion = 0
#         lessons.save()
        
#         response["result"] = "true"
#         response["status_code"] = "200"
#         response["message"] = "success"
#         response["data"] = 1

#     return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})






# # 진행중인 레슨
# @swagger_auto_schema(
#     method='POST',
#     operation_id='지금 레슨 ?',
#     operation_description='수강생을 등록 합니다.',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#     ),
#     tags=['hypeboy'],
#     responses={200: openapi.Response(
#         description="200 OK",
#         schema=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
#                 'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
#             }
#         )
#     )}
# )
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JWTAuthentication,))
# def nowLesson(request):

#     today = DateFormat(datetime.now()).format('Ymd')

#     response = {}
#     data = {}

#     # 토큰으로 유저 email 가져오기
#     email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

#     # 유저 정보
#     user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))


#     if not user_info :

#         response["result"] = "true"
#         response["status_code"] = "800"
#         response["message"] = "유저 정보 없음"
#         response["data"] = []

#     else :
#         user_id = user_info[0]['fields']['user_id']


#         today = DateFormat(datetime.now()).format('Ymd')
#         member = Member.objects.filter(id=user_id)
#         lessons = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))

#         member = json.loads(serializers.serialize('json', Member.objects.filter(id = user_id)))
#         lessons = json.loads(serializers.serialize('json', Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1).order_by('completion', '-id', '-create_date')))

#         if not member :
#             data["member"] = []
#         else :
#             data["member"] = member[0]['fields']

#         if not lessons :
#             data["lessons"] = []
#         else :
#             data["lessons"] = lessons[0]['fields']

#         data["today"] = today

#         response["result"] = "true"
#         response["status_code"] = "200"
#         response["message"] = "success"
#         response["data"] = data


#     return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})



# @swagger_auto_schema(
#     method='POST',
#     operation_id='레슨 추가',
#     operation_description='수강생을 등록 합니다.',
#     request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'set': openapi.Schema(type=openapi.TYPE_STRING, description="회원 이름"),
#             'name': openapi.Schema(type=openapi.TYPE_STRING, description="회원 키"),
#             'weight': openapi.Schema(type=openapi.TYPE_STRING, description="회원 몸무게"),
#             'count': openapi.Schema(type=openapi.TYPE_STRING, description="회원 성별"),
#             'today': openapi.Schema(type=openapi.TYPE_STRING, description="회원 성별"),
#         }
#     ),
#     tags=['hypeboy'],
#     responses={200: openapi.Response(
#         description="200 OK",
#         schema=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
#                 'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
#             }
#         )
#     )}
# )
# @api_view(['POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JWTAuthentication,))
# def addLesson(request):

#     response = {}

#     # 토큰으로 유저 email 가져오기
#     email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

#     # 유저 정보
#     user_info = json.loads(serializers.serialize('json', Member.objects.filter(user_email=email)))

#     if not user_info :
#         response["result"] = "true"
#         response["status_code"] = "800"
#         response["message"] = "유저 정보 없음"
#         response["data"] = []
#     elif not request.data["set"] :
#         response["result"] = "true"
#         response["status_code"] = "801"
#         response["message"] = "set 값이 없습니다."
#         response["data"] = 0
#     elif not request.data['name'] :
#         response["result"] = "true"
#         response["status_code"] = "802"
#         response["message"] = "name 값이 없습니다."
#         response["data"] = 0
#     elif not request.data['weight'] :
#         response["result"] = "true"
#         response["status_code"] = "803"
#         response["message"] = "weight 값이 없습니다."
#         response["data"] = 0
#     elif not request.data['count'] :
#         response["result"] = "true"
#         response["status_code"] = "804"
#         response["message"] = "count 값이 없습니다."
#         response["data"] = 0
#     elif not request.data['todat'] :
#         response["result"] = "true"
#         response["status_code"] = "804"
#         response["message"] = "todat 값이 없습니다."
#         response["data"] = 0
#     else :
#         user_id = user_info[0]['fields']['user_id']

#         for i in range(1, int(request.data['set'])+1) :
#             lesson = Lesson()
#             lesson.user_id = user_id
#             lesson.name = request.data['name']
#             lesson.weight = request.data['weight']
#             lesson.count = request.data['count']
#             lesson.set = i
#             lesson.start_date = request.data['today']
#             lesson.create_date = timezone.datetime.now()
#             lesson.save()

#         response["result"] = "true"
#         response["status_code"] = "200"
#         response["message"] = "success"
#         response["data"] = 1


#     return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

