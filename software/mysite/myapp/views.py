

# Create your views here.
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, redirect
import json
from .models import Student
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
    return render(request, 'myapp/homepage.html',{'name': name})
    



def coursesearch(request):
    if request.method == 'POST':
        uid = request.session.get('uid')
        name = request.session.get('name')
        if uid and name:
            # 成功驗證 session，返回成功狀態
            return JsonResponse({'status': True})
            #return render(request, 'myapp/coursesearch.html')
        else:
            # 若 session 中沒有 uid 和 name，則返回失敗狀態並跳轉到登入頁面
            return JsonResponse({'status': False, 'msg': '尚未登入，請重新登入'})

    # 若請求非 POST，則渲染課程查詢頁面
    


