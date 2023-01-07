from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.db.models import Count

from .models import Lesson
 
# Create your views here.
def hypeboy(request):
    return render(request, 'hypeboy.html')

def lessonAdd(request):
    return render(request, 'lessonAdd.html')

def lessonIng(request, user_id):
    lessons = Lesson.objects.filter(user_id=user_id).values('start_date').annotate(entries=Count('start_date'))
    return render(request, 'lessonIng.html', {'lessons': lessons, 'user_id' : user_id})

def lessonNow(request, user_id, start_date):
    lessons = Lesson.objects.filter(user_id=user_id, start_date=start_date, view_yn=1).order_by('completion', '-id', '-create_date')
    print(lessons)
    return render(request, 'lessonNow.html', {'lessons': lessons, 'user_id' : user_id})

def lessonEnd(request):
    return render(request, 'lessonEnd.html')

# 레슨 추가
def add(request):
    today = DateFormat(datetime.now()).format('Ymd')

    lesson = Lesson()
    lesson.user_id = 1
    lesson.name = request.GET['name']
    lesson.weight = request.GET['weight']
    lesson.count = request.GET['count']
    lesson.set = request.GET['set']
    lesson.start_date = today
    lesson.create_date = timezone.datetime.now()
    lesson.save()

    return redirect('lessonNow', user_id=1, start_date=today)

# 운동 미노출 처리
def delete(request, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)
    lessons.view_yn = 0
    lessons.save()
    
    return redirect('lessonNow', user_id=1, start_date=today)

# 운동 완료 처리
def completion(request, lesson_id):

    today = DateFormat(datetime.now()).format('Ymd')

    lessons = Lesson.objects.get(id=lesson_id)

    lessons.completion = 1
    lessons.save()
    
    return redirect('lessonNow', user_id=1, start_date=today)   