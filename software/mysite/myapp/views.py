

# Create your views here.
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, redirect
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
    

from django.shortcuts import render, redirect
from .models import Course

def coursesearch(request):
    uid = request.session.get('uid')
    name = request.session.get('name')

    if uid and name:
        if request.method == 'GET':
            # 獲取所有查詢條件
            course_name = request.GET.get('course_name', '')
            course_code = request.GET.get('course_code', '')
            department = request.GET.get('department', '')
            time = request.GET.get('time', '')
            teacher = request.GET.get('teacher', '')
            language = request.GET.get('language', '')
            course_type = request.GET.get('course_type', '')

            # 根據選中的條件篩選課程資料
            courses = Course.objects.all()

            if request.GET.get('search_name') and course_name:
                courses = courses.filter(name__icontains=course_name)  # 模糊查詢課程名稱
            if request.GET.get('search_code') and course_code:
                courses = [course for course in courses if str(course.id).startswith(course_code)]  # 部分匹配課程代碼
            if request.GET.get('search_department') and department:
                courses = courses.filter(department__icontains=department)  # 模糊查詢開課系所
            if request.GET.get('search_time') and time:
                courses = courses.filter(time__icontains=time)  # 模糊查詢修課時段
            if request.GET.get('search_teacher') and teacher:
                courses = courses.filter(teacher__icontains=teacher)  # 模糊查詢授課教師
            if request.GET.get('search_language') and language:
                courses = courses.filter(language__icontains=language)  # 模糊查詢授課語言
            if request.GET.get('search_type') and course_type:
                courses = courses.filter(type__icontains=course_type)  # 模糊查詢課程種類

            # 準備將課程和生成的課程代碼一起傳遞到模板
            courses_with_code = [
                {
                    'course': course,
                    'course_code': f"{course.id}"  # 生成課程代碼
                }
                for course in courses
            ]

            # 傳遞結果到模板
            return render(request, 'myapp/coursesearch.html', {
                'name': name,
                'courses_with_code': courses_with_code,
                'course_name': course_name,
                'course_code': course_code,
                'department': department,
                'time': time,
                'teacher': teacher,
                'language': language,
                'course_type': course_type
            })
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
        
        # 從 Curriculum 表中取得所有課程對應的課程名稱
        course_names = [entry.course_id.name for entry in curriculum_entries]
        
    except Student.DoesNotExist:
        return HttpResponse("學生不存在")
    
    # 將課程名稱列表傳遞到模板中
    return render(request, 'myapp/selected_courses.html', {'course_names': course_names, 'name': student.name})
#fesgse

