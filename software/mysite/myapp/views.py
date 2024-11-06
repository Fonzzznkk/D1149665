

# Create your views here.
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, redirect
import json
from .models import Student,Curriculum
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
        
        # 從 Curriculum 表中取得所有課程對應的課程名稱
        course_names = [entry.course_id.name for entry in curriculum_entries]
        
    except Student.DoesNotExist:
        return HttpResponse("學生不存在")
    
    # 將課程名稱列表傳遞到模板中
    return render(request, 'myapp/selected_courses.html', {'course_names': course_names, 'name': student.name})

