from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # รวม URL จากแอป vercel และตั้งให้เป็นหน้าหลัก
    path("", include("vercel.urls")),
]