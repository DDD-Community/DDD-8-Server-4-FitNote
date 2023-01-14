from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.db.models import Count
from django.http import JsonResponse
from rest_framework_simplejwt.models import TokenUser

from .models import Lesson
from attention.views import getUser
from attention.models import Member


# Create your views here.
def hypeboy(request):
    return render(request, 'hypeboy.html')

def lessonAdd(request, user_id):
    today = DateFormat(datetime.now()).format('Ymd')
    member = Member.objects.filter(user_id=user_id)
    return render(request, 'lessonAdd.html', {'member' : member[0], 'today' : today})

def lessonIng(request, user_id):
    today = DateFormat(datetime.now()).format('Ymd')
    member = Member.objects.filter(user_id=user_id)
    lessons = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))
    lessons_name_list = Lesson.objects.filter(user_id=user_id, start_date=lessons[0]['start_date'], view_yn=1).values('name').annotate(entries=Count('name'))
    return render(request, 'lessonIng.html', {'member': member[0], 'lessons' : lessons, 'today' : today, 'lessons_name_list' : lessons_name_list})

def lessonNow(request, user_id, today):
    member = Member.objects.filter(user_id=user_id)
    lessons = Lesson.objects.filter(user_id=user_id, start_date=today, view_yn=1).order_by('completion', '-id', '-create_date')
    return render(request, 'lessonNow.html', {'lessons': lessons, 'user_id' : user_id, 'member' : member[0]})

def lessonEnd(request):
    return render(request, 'lessonEnd.html')

# 레슨 추가
def add(request, user_id, today):
    today = DateFormat(datetime.now()).format('Ymd')

    lesson = Lesson()
    lesson.user_id = user_id
    lesson.name = request.GET['name']
    lesson.weight = request.GET['weight']
    lesson.count = request.GET['count']
    lesson.set = request.GET['set']
    lesson.start_date = today
    lesson.create_date = timezone.datetime.now()
    lesson.save()

    return redirect('lessonNow', user_id=user_id, start_date=today)

# 운동 미노출 처리
def delete(request, user_id, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)
    lessons.view_yn = 0
    lessons.save()
    
    return redirect('lessonNow', user_id=user_id, start_date=today)

# 운동 완료 처리
def completion(request, user_id, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)

    lessons.completion = 1
    lessons.save()
    
    return redirect('lessonNow', user_id=user_id, start_date=today)


def schedule(request):

    email = getUser(request.META['HTTP_AUTHORIZATION'][7:])

    member = Member.objects.filter(user_email=email)

    print(member)

    today = DateFormat(datetime.now()).format('Ymd')
    # member = Member.objects.filter(user_id=user_id)
    # lessons = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))
    # lessons_name_list = Lesson.objects.filter(user_id=user_id, start_date=lessons[0]['start_date'], view_yn=1).values('name').annotate(entries=Count('name'))

    response = {}

    response["result"] = "true"
    response["status_code"] = "200"
    response["message"] = "성공!"

    return JsonResponse(response, json_dumps_params = {'ensure_ascii': False})
