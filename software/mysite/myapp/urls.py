from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world),
    path('login/', views.loginpage),
    path('homepage/', views.homepage),
    path('coursesearch/', views.coursesearch),
    path('selected_courses/', views.selected_courses_view, name='selected_courses'),
    path('course_mydetail/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/add/', views.add_course, name='add_course'),
    path('course/<int:course_id>/drop/', views.drop_course, name='drop_course'),
]

