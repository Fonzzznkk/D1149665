

# Create your views here.
from ctypes import sizeof
from django.http import HttpResponse
import os
from django.shortcuts import render, redirect, get_object_or_404
import json
from .models import Student,Curriculum,Course
from django.http import JsonResponse
from collections import defaultdict

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
        return render(request, 'myapp/homepage.html', {'name': name, 'uid': uid})
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
                'uid': uid,
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
    uid = request.session.get('uid')
    name = request.session.get('name')
    
    # 若沒有 uid，返回提示訊息
    if not uid:
        return HttpResponse("請先登入")  
    
    try:
        # 獲取當前學生
        student = Student.objects.get(student_id=uid)
        # 獲取學生的所有課程
        curriculum_entries = Curriculum.objects.filter(student_id=student.id)
        # 將課程名稱和時間分別存入列表中
        courses = [(entry.course_id.name, entry.course_id.time) for entry in curriculum_entries]
        
        # 初始化字典來存儲課表資料
        #timetable = defaultdict(lambda: [''] * 13)  # 每天有 13 節課
        timetable = defaultdict(lambda: [[] for _ in range(13)])

        # 解析時間並將課程分配到 timetable
        for course_name, time in courses:
            # 假設時間格式為 "(一)06(一)07"
            time_slots = time.split('(')
            for time_slot in time_slots:
                if time_slot:
                    try:
                        # 拆解為星期和節次
                        day, period = time_slot.split(')')
                        day = day.strip()
                        period = int(period.strip()) - 1  # 將 period 轉為索引
                        
                        if day in ['一', '二', '三', '四', '五', '六', '日'] and 0 <= period < 13:
                            # 填入課程名稱至對應的星期和節次中
                            timetable[day][period].append(course_name)
                        else:
                            print(f"Warning: Invalid day or period for course '{course_name}': '{time_slot}'")
                    except ValueError:
                        print(f"Warning: Invalid time format for course '{course_name}': '{time_slot}'")
        
        # 設定星期的順序
        days_of_week = ['一', '二', '三', '四', '五', '六', '日']
        
    except Student.DoesNotExist:
        return HttpResponse("學生不存在")

    # 生成節次列表
    periods = list(range(1, 14))

    # 渲染模板
    return render(request, 'myapp/selected_courses.html', {
        'name': student.name,
        'uid': uid,
        'timetable': timetable,
        'days_of_week': days_of_week,
        'periods': periods

    })




def course_detail(request, course_id):
    # 根據 URL 中的 course_id 從資料庫中獲取對應的課程
    course = get_object_or_404(Course, id=course_id)
    
    # 將課程資料傳遞給模板
    return render(request, 'myapp/course_detail.html', {'course': course})


def course_detail_redirect(request):
    if request.method == "POST":
        data = json.loads(request.body)
        course_name = data.get("course_name")
        student_name = data.get("student_name")

        # 根據 student_name 查找對應的 Student
        student = get_object_or_404(Student, name=student_name)

        # 查找課程並驗證是否屬於該學生的課程
        try:
            course = Course.objects.get(name=course_name)
            curriculum = Curriculum.objects.get(student_id=student, course_id=course)

            # 成功時返回課程的 ID
            return JsonResponse({"success": True, "course_id": course.id})
        except (Course.DoesNotExist, Curriculum.DoesNotExist):
            return JsonResponse({"success": False, "error": "課程資料未找到"})

    return JsonResponse({"success": False, "error": "無效的請求"})


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
        # 檢查是否存在衝堂的課程
        conflict_courses = []
        
        # 將新增課程的上課時間取出
        new_course_time = course.time.split('(')  # 假設時間格式為 "(一)06(一)07"
        new_course_slots = set()  # 儲存新加選課程的所有時段
        
        for time_slot in new_course_time:
            if time_slot:
                day, period = time_slot.split(')')
                day = day.strip()
                period = period.strip()
                new_course_slots.add((day, period))
        
        # 取得學生已選的所有課程
        existing_courses = Curriculum.objects.filter(student_id=student)
        
        # 檢查每個已選課程是否與新加選課程時間衝突
        for entry in existing_courses:
            existing_course = entry.course_id
            existing_course_time = existing_course.time.split('(')
            
            for time_slot in existing_course_time:
                if time_slot:
                    day, period = time_slot.split(')')
                    day = day.strip()
                    period = period.strip()
                    
                    # 檢查是否存在衝突
                    if (day, period) in new_course_slots:
                        conflict_courses.append(existing_course.name)
                        break  # 若衝堂，則跳出檢查
                        
        # 返回結果
        count = 0
        for i in conflict_courses:
            count+=1
        if count>1:
            conflict_message = "加選成功，但發現以下課程衝堂：" + ", ".join(conflict_courses)
            return HttpResponse(conflict_message)
        else:
            return HttpResponse("成功加選課程")
    else:
        return HttpResponse("課程已加選，無需重複操作")


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

