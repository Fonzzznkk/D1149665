from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_world),
    path('login/', views.loginpage),
    path('homepage/', views.homepage),
    path('coursesearch/', views.coursesearch, name='coursesearch'),
    path('selected_courses/', views.selected_courses_view, name='selected_courses'),
]

