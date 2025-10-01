import os
from django.shortcuts import render, get_object_or_404
import json
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .utils import load_temple_data, get_temple_by_name

# Create your views here.

def home(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'home.html', {'api_key': api_key})

def about(request):
    try:
        return render(request, 'about.html')
    except Exception as e:
        # Log the error for debugging
        print(f"Error in about view: {str(e)}")
        return JsonResponse({'error': f'Template error: {str(e)}'}, status=500)

def map_view(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'map.html', {'api_key': api_key})

def places(request):
    try:
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        
        # Use the utility function to load data
        data = load_temple_data()
        
        # Convert Thai field names to English for template compatibility
        sites = []
        for site in data.get('ancient_sites_sisaket', []):
            converted_site = {
                'name': site['ชื่อสถานที่'],
                'organization': site.get('อปท.', ''),
                'district': site['อำเภอ'],
                'province': site['จังหวัด'],
                'address': site['ที่อยู่'],
                'lat': site['LAT'],
                'lng': site['LONG'],
                'image': site['image']
            }
            sites.append(converted_site)
        
        context = {
            'sites': sites,
            'api_key': api_key
        }
        return render(request, 'places.html', context)
    except Exception as e:
        # Log the error for debugging  
        print(f"Error in places view: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': f'View error: {str(e)}'}, status=500)

def temple_detail_map(request, temple_name):
    """Display individual temple location on map"""
    try:
        # Decode URL-encoded temple name
        from urllib.parse import unquote
        temple_name = unquote(temple_name)
        print(f"Looking for temple: {temple_name}")
        
        # Use the utility function to get temple data
        temple_data = get_temple_by_name(temple_name)
        
        if not temple_data:
            # Get all available temple names for debugging
            data = load_temple_data()
            available_temples = [site['ชื่อสถานที่'] for site in data.get('ancient_sites_sisaket', [])]
            print(f"Available temples: {available_temples}")
            raise Http404(f"Temple '{temple_name}' not found. Available temples: {', '.join(available_temples)}")
        
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
            'image': f"images/location/{temple_data['image']}",  # Fixed path
            'organization': temple_data.get('อปท.', temple_data.get('ตำบล', '')),
        }
        
        context = {
            'temple': temple,
            'api_key': api_key,
            'temple_lat': temple['lat'],
            'temple_lng': temple['lng'],
        }
        
        return render(request, 'temple_detail_map.html', context)
    
    except Exception as e:
        print(f"Error in temple_detail_map: {str(e)}")
        import traceback
        print(traceback.format_exc())
        raise Http404(f"Error loading temple detail: {str(e)}")

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