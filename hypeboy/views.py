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

from django.core import serializers
from django.http import JsonResponse
from django.db.models import Sum
import itertools, logging

# 공유하기 페이지
def share(request, user_id, today):

    # 테스트 Url http://127.0.0.1:8000/hypeboy/share/48/20230330

    lessons = Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1)

    trainer_id = Member.objects.filter(id=user_id).values_list('trainer_group', flat=True)[0]

    trainer_name = Member.objects.filter(id=trainer_id).values_list('user_name', flat=True)[0]

    user_name = Member.objects.filter(id=user_id).values_list('user_name', flat=True)[0]

    today = str(today)

    year = today[0:4]
    month = today[4:6]
    date = today[6:8]

    # 공유하기 운동 이름 그룹 바이 처리 
    lessons_name = list(Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1).values('name').annotate(entries=Count('name')))

    queryset = Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1).values('id', 'name', 'weight', 'count', 'set')

    result = []
    for key, group in itertools.groupby(queryset, key=lambda x: x['name']):
        item = {'name': key, 'list': []}
        for g in group:
            item['list'].append({'id': g['id'], 'set': g['set'], 'count': g['count'], 'weight': g['weight']})
        result.append(item)

    context = {
        'result': result
        , 'trainer_name' : trainer_name
        , 'user_name' : user_name
        , 'year' : year
        , 'month' : month
        , 'date' : date
    }

    return render(request, 'share.html', context=context)

######################################################### 회원의 예정된 수업 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='예정된 수업',
    operation_description=
        '트레이너가 회원의 예정된 수업을 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=294%3A5057&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키(user_id)"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
                'getLessonInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="lessons_date : 수업 시작 날짜, \n lessons_name : 수업 운동 이름"),
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

            lessons_list = Lesson.objects.filter(user_id=request.data['id'], total_completion=0).values('start_date').annotate(entries=Count('start_date'))

            if not lessons_list :
                data["lessons_list"] = []
                data["exercise_list"] = []
            else :

                data['getLessonInfo'] = []

                setName = []
                for i in range(0, int(len(lessons_list))) :

                    date = lessons_list[i]['start_date']
                
                    name = list(Lesson.objects.filter(user_id=request.data['id'], start_date=lessons_list[i]['start_date'], view_yn=1, total_completion=0).values('name').annotate(entries=Count('name')))

                    for j in range(0, int(len(name))):
                        setName.append(name[j]['name'])

                    data['getLessonInfo'].append({
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
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키(user_id)"),
            'today': openapi.Schema(type=openapi.TYPE_STRING, description="운동 날짜 YYYYMMDD ex)20220101"),
            'set': openapi.Schema(type=openapi.TYPE_INTEGER, description="운동 세트"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="운동 이름"),
            'weight': openapi.Schema(type=openapi.TYPE_STRING, description="운둥 중량"),
            'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="운동 횟수"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 7xx: 실패"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def addLesson(request):

    response = {}

    if not request.data :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "id 값이 없습니다."
        response["data"] = []

        return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})

    getMemberInfo = json.loads(serializers.serialize('json', Member.objects.filter(id=request.data['id'])))

    # 원하는 위치에 로그를 남깁니다.
    logger = logging.getLogger('django.request')
    data_type = type(request.data["lessonList"])

    logger.debug(request.data["lessonList"])
    logger.debug(data_type)

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
            elif not request.data['today'] :
                response["result"] = "true"
                response["status_code"] = "802"
                response["message"] = "today 값이 없습니다."
                response["data"] = 0
            elif not request.data['name'] :
                response["result"] = "true"
                response["status_code"] = "803"
                response["message"] = "name 값이 없습니다."
                response["data"] = 0
            elif not request.data['weight'] :
                response["result"] = "true"
                response["status_code"] = "804"
                response["message"] = "weight 값이 없습니다."
                response["data"] = 0
            elif not request.data['count'] :
                response["result"] = "true"
                response["status_code"] = "805"
                response["message"] = "count 값이 없습니다."
                response["data"] = 0
            else :
                lesson = Lesson()
                lesson.user_id = request.data['id']
                lesson.name = request.data['name']
                lesson.weight = request.data['weight']
                lesson.count = request.data['count']
                lesson.set = request.data['set']
                lesson.start_date = request.data['today']
                lesson.create_date = timezone.datetime.now()
                lesson.save()

                response["result"] = "true"
                response["status_code"] = "200"
                response["message"] = "success"
                response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 추가 END #########################################################

######################################################### 회원의 예정된 수업 종료 START #########################################################
@swagger_auto_schema(
    method='DELETE',
    operation_id='회원 수업 추가',
    operation_description=
        '회원의 수업을 추가합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2770&t=9sYn60yjGqRDPLux-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'lesson_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="레슨 id"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 7xx: 실패"),
            }
        )
    )}
)
@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def deleteLesson(request):

    response = {}

    if not request.data["lesson_id"] :
        response["result"] = "true"
        response["status_code"] = "700"
        response["message"] = "트레이너 회원 입니다."
        response["data"] = []
    else :
        lessons = Lesson.objects.get(id=request.data["lesson_id"])
        lessons.view_yn = 0
        lessons.save()
        
        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 종료 END #########################################################

######################################################### 회원의 예정된 수업 Update START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='회원 수업 수정',
    operation_description=
        '회원의 수업을 수정합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키(user_id)"),
            'today': openapi.Schema(type=openapi.TYPE_STRING, description="운동 날짜 YYYYMMDD ex)20220101"),
            'set': openapi.Schema(type=openapi.TYPE_INTEGER, description="운동 세트"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="운동 이름"),
            'weight': openapi.Schema(type=openapi.TYPE_STRING, description="운둥 중량"),
            'count': openapi.Schema(type=openapi.TYPE_INTEGER, description="운동 횟수"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 7xx: 실패"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def updateLesson(request):

    today = DateFormat(datetime.now()).format('Ymd')

    response = {}

    if not request.data["set"] :
        response["result"] = "true"
        response["status_code"] = "801"
        response["message"] = "set 값이 없습니다."
        response["data"] = 0
    else :
        lesson = Lesson.objects.get(id=request.data["lesson_id"])
        lesson.user_id = request.data['id']
        lesson.name = request.data['name']
        lesson.weight = request.data['weight']
        lesson.count = request.data['count']
        lesson.start_date = request.data['today']
        lesson.create_date = timezone.datetime.now()
        lesson.save()
        
        response["result"] = "true"
        response["status_code"] = "200"
        response["message"] = "success"
        response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 예정된 수업 Update END #########################################################

######################################################### 회원의 종료된 수업 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='종료된 수업',
    operation_description=
        '트레이너가 회원의 종료된 수업을 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2672&t=2etd924LSzcLvhk6-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키(user_id)"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
                'getLessonInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="lessons_date : 수업 시작 날짜, \n lessons_name : 수업 운동 이름"),
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

            lessons_list = Lesson.objects.filter(user_id=request.data['id'], total_completion=1).values('start_date').annotate(entries=Count('start_date'))

            if not lessons_list :
                data["lessons_list"] = []
                data["exercise_list"] = []
            else :

                data['getLessonInfo'] = []

                setName = []
                for i in range(0, int(len(lessons_list))) :

                    date = lessons_list[i]['start_date']
                
                    name = list(Lesson.objects.filter(user_id=request.data['id'], start_date=lessons_list[i]['start_date'], view_yn=1, total_completion=1).values('name').annotate(entries=Count('name')))

                    for j in range(0, int(len(name))):
                        setName.append(name[j]['name'])

                    data['getLessonInfo'].append({
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


######################################################### 회원의 수업 상세 START #########################################################
@swagger_auto_schema(
    method='POST',
    operation_id='수업 상세',
    operation_description=
        '트레이너가 회원의 예정된 수업을 가져옵니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=294%3A5057&t=suTWrwzQMntuXORc-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 키(user_id)"),
            'today': openapi.Schema(type=openapi.TYPE_INTEGER, description="레슨 진행 날짜(key)"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'getMemberInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="user_id : 회원 고유 키, \n user_name : 회원 이름, \n user_email : 회원 이메일, \n user_type : 회원 타입 (1: 트레이너, 2: 일반 회원), \n trainer_group : 트레이너 고유 키(트레이너의 회원), \n user_height : 회원 키, \n user_weight : 회원 몸무게, \n user_status : 회원 상태 (1: 활성, 2: 탈퇴), \n user_view : 회원 노출 상태 (1: 노출, 2: 미노출), \n user_gender : 회원 성별 (1: 남성, 2: 여성), \n create_date : 데이터 생성 시점, \n update_date : 데이터 수정 시점, \n id : 회원 고유 키(운동 리스트에 사용)"),
                'getLessonInfo': openapi.Schema(type=openapi.TYPE_OBJECT, description="lessons_date : 수업 시작 날짜, \n lessons_name : 수업 운동 이름"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def getLesson(request):

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
        elif not request.data["today"] :
            response["result"] = "true"
            response["status_code"] = "701"
            response["message"] = "today 값이 없습니다."
            response["data"] = []
        else :

            getMemberInfo[0]['fields']['id'] = Member.objects.filter(id=request.data['id'], user_type=2).values_list('id', flat=True).order_by('-id')[0]

            data["getMemberInfo"] = getMemberInfo[0]['fields']

            lessons_list = list(json.loads(serializers.serialize('json', Lesson.objects.filter(user_id=request.data['id'], start_date=request.data["today"], view_yn=1))))

            # data['getLessonInfo'] = getLessonInfo[0]['fields']
            data["getLessonInfo"] = []
            name = []
            for i in range(0, int(len(lessons_list))) :

                # # pk 강제 삽입
                lessons_json = lessons_list[i]['fields']
                lessons_json['lesson_id'] = lessons_list[i]['pk']

                name.append(lessons_json)
                
                data['getLessonInfo'].append(name)

                name = []

            response["result"] = "true"
            response["status_code"] = "200"
            response["message"] = "success"
            response["data"] = data

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 수업 상세 END #########################################################

######################################################### 회원의 수업 완료 START #########################################################
@swagger_auto_schema(
    method='PUT',
    operation_id='회원 수업 완료',
    operation_description=
        '회원의 수업을 완료합니다. >> https://www.figma.com/file/9A22UfWb1Kmt8gwr11u0I9/GUI?node-id=163%3A2770&t=9sYn60yjGqRDPLux-4',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="회원 id"),
            'lesson_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="레슨 id"),
            'today': openapi.Schema(type=openapi.TYPE_INTEGER, description="레슨 시작 날짜"),
        }
    ),
    tags=['hypeboy'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'data': openapi.Schema(type=openapi.TYPE_INTEGER, description="1: 성공, 7xx: 실패"),
            }
        )
    )}
)
@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))
def completionLesson(request):

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
            if not request.data["lesson_id"] :
                response["result"] = "true"
                response["status_code"] = "801"
                response["message"] = "set 값이 없습니다."
                response["data"] = 0
            elif not request.data["today"] :
                response["result"] = "true"
                response["status_code"] = "801"
                response["message"] = "set 값이 없습니다."
                response["data"] = 0
            else :
                            
                lessons = Lesson.objects.get(id=request.data["lesson_id"])

                lessons.completion = 1
                lessons.save()

                completion_check = Lesson.objects.filter(user_id=request.data["id"], start_date=request.data["today"], completion=0)

                if not completion_check :
                    completion_go = Lesson.objects.filter(user_id=request.data["id"], start_date=request.data["today"], completion=1)
                    for i in range(0, len(completion_go)):
                        completion_go[i].total_completion = 1
                        completion_go[i].save()
                
                response["result"] = "true"
                response["status_code"] = "200"
                response["message"] = "success"
                response["data"] = 1

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
######################################################### 회원의 수업 완료 END #########################################################
