"""
URL configuration for sisaket project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# 1. Import built-in views ของ Django สำหรับการยืนยันตัวตน
from django.contrib.auth import views as auth_views
from vercel import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # URL ของหน้าหลักต่างๆ
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("map/", views.map_view, name="map"),
    path("places/", views.places, name="places"),

    # 2. เพิ่ม URL สำหรับ Login, Logout, และ Register
    path('auth/', views.auth_view, name='auth'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
