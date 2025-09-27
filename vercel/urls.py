from django.urls import path
from . import views

urlpatterns = [
    # หน้าแรกจะใช้ auth_view
    path('', views.auth_view, name='auth'),
    path('home/', views.home_view, name='home'),
    path('places/', views.places_view, name='places'),
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
]