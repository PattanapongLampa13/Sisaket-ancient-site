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
from vercel import views
from django.conf import settings             # 1. import settings
from django.conf.urls.static import static   # 2. import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("map/", views.map_view, name="map"),
    path("places/", views.places, name="places"),
    path("temple/<str:temple_name>/", views.temple_detail_map, name="temple_detail_map"),
    path("register/", views.register, name="register"),
]
