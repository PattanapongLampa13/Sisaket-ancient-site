from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def auth_view(request):
    if request.user.is_authenticated:
        return redirect('home') # เปลี่ยนให้ไปหน้า home หลังล็อกอิน

    if request.method == 'POST':
        # ตรวจสอบว่าเป็นฟอร์มล็อกอินหรือไม่
        if 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home') # เปลี่ยนให้ไปหน้า home หลังล็อกอิน
                else:
                    messages.error(request, 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง')
            else:
                messages.error(request, 'ข้อมูลล็อกอินไม่ถูกต้อง')
            # ส่ง register_form ที่ว่างเปล่าไปด้วย
            register_form = CustomUserCreationForm()
        else: # ถ้าไม่ใช่ฟอร์มล็อกอิน ก็เป็นฟอร์มสมัครสมาชิก
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('home') # เปลี่ยนให้ไปหน้า home หลังล็อกอิน
            else:
                messages.error(request, 'ข้อมูลการสมัครไม่ถูกต้อง กรุณาตรวจสอบอีกครั้ง')
            # ส่ง login_form ที่ว่างเปล่าไปด้วย
            login_form = CustomAuthenticationForm()
    else:
        login_form = CustomAuthenticationForm()
        register_form = CustomUserCreationForm()

    # ตรวจสอบว่าควรแสดงแท็บไหน
    # ถ้ามี error ใน register_form ให้แสดงแท็บ register
    initial_tab = 'register' if 'register_form' in locals() and register_form.errors else 'login'

    return render(request, 'auth.html', {
        'login_form': login_form,
        'register_form': register_form,
        'initial_tab': initial_tab
    })

@login_required
def home_view(request):
    # หน้านี้จะแสดงหลังจาก login และจะเล่น animation
    return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'คุณออกจากระบบเรียบร้อยแล้ว')
    return redirect('auth')

@login_required
def places_view(request):
    return render(request, 'places.html')

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'บัญชีของคุณถูกลบเรียบร้อยแล้ว')
        return redirect('auth') # กลับไปหน้า auth
    return render(request, 'delete_account.html')