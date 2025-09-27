from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_protect

def home(request):
    """
    View สำหรับหน้าแรก
    """
    context = {'api_key': settings.GOOGLE_MAPS_API_KEY}
    # คุณอาจจะต้องเปลี่ยน 'home.html' เป็นชื่อ template ที่ถูกต้องสำหรับหน้าแรกของคุณ
    return render(request, 'base.html', context)

def about(request):
    """
    View สำหรับหน้า 'เกี่ยวกับ'
    """
    context = {'api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'about.html', context)

def map_view(request):
    """
    View สำหรับหน้าแผนที่
    """
    context = {'api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'map.html', context)

def places(request):
    """
    View สำหรับหน้าสถานที่
    """
    context = {'api_key': settings.GOOGLE_MAPS_API_KEY}
    return render(request, 'places.html', context)


# Combined auth view
@csrf_protect
def auth_view(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST and 'login' in request.POST:
            # Login form submitted
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')
        elif 'username' in request.POST and 'password1' in request.POST and 'password2' in request.POST:
            # Register form submitted
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'สร้างบัญชีสำเร็จแล้ว! กรุณาเข้าสู่ระบบ')
                return redirect('auth')
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'api_key': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'auth.html', context)

# Redirect /login/ and /register/ to /auth/ and set tab
from django.http import HttpResponseRedirect
def login_redirect(request):
    return HttpResponseRedirect('/auth/?tab=login')
def register_redirect(request):
    return HttpResponseRedirect('/auth/?tab=register')

@csrf_protect
def login_view(request):
    login_form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and login_form.is_valid():
        user = login_form.get_user()
        auth_login(request, user)
        return redirect('home')
    return render(request, 'login.html', {'login_form': login_form, 'api_key': settings.GOOGLE_MAPS_API_KEY})

@csrf_protect
def register_view(request):
    register_form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and register_form.is_valid():
        register_form.save()
        messages.success(request, 'สร้างบัญชีสำเร็จแล้ว! กรุณาเข้าสู่ระบบ')
        return redirect('login')
    return render(request, 'register.html', {'register_form': register_form, 'api_key': settings.GOOGLE_MAPS_API_KEY})