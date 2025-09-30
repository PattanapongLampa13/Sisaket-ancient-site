import os
from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse, Http404
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
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'map.html', {'api_key': api_key})

def places(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    context = {
        'sites': data['ancient_sites_sisaket'],
        'api_key': api_key
    }
    return render(request, 'places.html', context)

def temple_detail_map(request, temple_name):
    """Display individual temple location on map"""
    # Load temple data from JSON file
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Find the temple by name
    temple_data = None
    for site in data['ancient_sites_sisaket']:
        if site['ชื่อสถานที่'] == temple_name:
            temple_data = site
            break
    
    if not temple_data:
        raise Http404("Temple not found")
    
    # Get API key
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY_HERE')
    
    # Convert Thai field names to English for template compatibility
    temple = {
        'name': temple_data['ชื่อสถานที่'],
        'district': temple_data['อำเภอ'],
        'province': temple_data['จังหวัด'],
        'address': temple_data['ที่อยู่'],
        'lat': temple_data['LAT'],
        'lng': temple_data['LONG'],
        'image': temple_data['image'],
        'organization': temple_data.get('อปท.', temple_data.get('ตำบล', '')),
    }
    
    context = {
        'temple': temple,
        'api_key': api_key,
        'temple_lat': temple['lat'],
        'temple_lng': temple['lng'],
    }
    
    return render(request, 'temple_detail_map.html', context)

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