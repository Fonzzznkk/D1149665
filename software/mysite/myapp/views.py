

# Create your views here.
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import Student,Curriculum,Course
from django.http import JsonResponse


def hello_world(request):
    return HttpResponse("Hello, world!")

#def loginpage(request):
#    return render(request, 'myapp/login.html')  # 路徑包含應用名稱

# 登入
def loginpage(request):
    if request.method == 'GET':
        return render(request, 'myapp/login.html')
    elif request.method == 'POST':
        # 验证用户名密码是否正确，然后登陆存入session
        type = request.POST.get('type')
        print("Type received:", type)
        response = {'msg': '', 'status': False}

        uid = request.POST.get('uid')
        pwd = request.POST.get('pwd')
        if type == 'login':
            students = Student.objects.filter(student_id=uid, password=pwd)
            student = students.first()
            #if len(Student.objects.filter(student_id=uid, password=pwd)) != 0:
            if student:
                # 登录成功
                print(student.name)
                response['status'] = True
                request.session['uid'] = uid
                request.session['name'] = student.name
                return HttpResponse(json.dumps(response))
                pass
            else:
                # 登录失败
                response['msg'] = '用户名或者密码错误'
                return HttpResponse(json.dumps(response))
                pass
        

#主頁
def homepage(request):
    uid = request.session.get('uid')
    name = request.session.get('name')
    
    if not uid:
        return redirect('/myapp/login/')  # 未登入的用戶重定向到登入頁面
    if request.method == 'GET':
        return render(request, 'myapp/homepage.html',{'name': name})
    elif request.method == 'POST':
        type = request.POST.get('type')
        print("Type received:", type)
        
        response = {'msg': '', 'status': False} 
        response['status'] = True
        request.session['uid'] = uid
        request.session['name'] = name
        return HttpResponse(json.dumps(response))
        pass
    



def coursesearch(request):
   
    uid = request.session.get('uid')
    name = request.session.get('name')
    if uid and name:
        if request.method == 'GET':
            return render(request, 'myapp/coursesearch.html',{'name': name})
    else:
        return redirect('/myapp/login/')  # 未登入的用戶重定向到登入頁面

    
    
def selected_courses_view(request):
    # 從 session 中取得學生的 uid
    uid = request.session.get('uid')
    name = request.session.get('name')
    if not uid:
        return HttpResponse("請先登入")  # 若沒有 uid，返回提示訊息
    
    try:
        # 根據 student_id 查找 Student 記錄
        student = Student.objects.get(student_id=uid)
        
        # 查找 Curriculum 表中該學生的所有課程
        curriculum_entries = Curriculum.objects.filter(student_id=student.id)
        
        # 從 Curriculum 表中取得每個課程的名稱和 ID
        courses = [(entry.course_id.name, entry.course_id.id) for entry in curriculum_entries]
        
    except Student.DoesNotExist:
        return HttpResponse("學生不存在")
    
    # 將課程名稱和 ID 列表傳遞到模板中
    return render(request, 'myapp/selected_courses.html', {'courses': courses, 'name': student.name})



def course_detail(request, course_id):
    # 根據 URL 中的 course_id 從資料庫中獲取對應的課程
    course = get_object_or_404(Course, id=course_id)
    
    # 將課程資料傳遞給模板
    return render(request, 'myapp/course_detail.html', {'course': course})


def add_course(request, course_id):
    # 從 session 中取得學生的 uid
    uid = request.session.get('uid')
    if not uid:
        return HttpResponse("請先登入")  # 若未登入，返回提示訊息

    # 查找學生和課程的記錄
    student = get_object_or_404(Student, student_id=uid)
    course = get_object_or_404(Course, id=course_id)

    # 檢查是否已經有該課程的記錄，若無則添加
    curriculum_entry, created = Curriculum.objects.get_or_create(student_id=student, course_id=course)
    
    if created:
        message = "成功加選課程"
    else:
        message = "課程已加選，無需重複操作"
    
    return HttpResponse(message)


def drop_course(request, course_id):
    # 從 session 中取得學生的 uid
    uid = request.session.get('uid')
    if not uid:
        return HttpResponse("請先登入")  # 若未登入，返回提示訊息

    # 查找學生和課程的記錄
    student = get_object_or_404(Student, student_id=uid)
    course = get_object_or_404(Course, id=course_id)

    # 嘗試刪除該課程的記錄，若不存在則忽略
    curriculum_entry = Curriculum.objects.filter(student_id=student, course_id=course)
    
    if curriculum_entry.exists():
        curriculum_entry.delete()
        message = "成功退選課程"
    else:
        message = "未選此課程，無法退選"
    
    return HttpResponse(message)

