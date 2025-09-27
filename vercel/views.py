import os
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def home(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'home.html', {'api_key': api_key})

def about(request):
    return render(request, 'about.html')

def map_view(request):
    return render(request, 'map.html')

def places(request):
    return render(request, 'places.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({'status': 'error', 'message': 'Username and password are required.'}, status=400)

            try:
                # Use Django's User model to create a new user
                # This will automatically handle password hashing
                User.objects.create_user(username=username, password=password)
            except IntegrityError:
                # This error occurs if the username is already taken
                return JsonResponse({'status': 'error', 'message': 'This username is already taken.'}, status=400)

            return JsonResponse({'status': 'success', 'message': 'Registration successful!'})

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)