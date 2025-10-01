import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login
from django.http import Http404

from .utils import load_temple_data, get_temple_by_name

# Create your views here.

@login_required
def home(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'home.html', {'api_key': api_key})

@login_required
def about(request):
    return render(request, 'about.html')

@login_required
def map_view(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    return render(request, 'map.html', {'api_key': api_key})

@login_required
def places(request):
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
    data = load_temple_data()
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

@login_required
def temple_detail_map(request, temple_name):
    """Display individual temple location on map"""
    from urllib.parse import unquote
    temple_name = unquote(temple_name)
    
    temple_data = get_temple_by_name(temple_name)
    
    if not temple_data:
        raise Http404(f"Temple '{temple_name}' not found.")
    
    api_key = os.environ.get('GOOGLE_MAPS_API_KEY', 'YOUR_API_KEY_HERE')
    
    temple = {
        'name': temple_data['ชื่อสถานที่'],
        'district': temple_data['อำเภอ'],
        'province': temple_data['จังหวัด'],
        'address': temple_data['ที่อยู่'],
        'lat': temple_data['LAT'],
        'lng': temple_data['LONG'],
        'image': f"images/location/{temple_data['image']}",
        'organization': temple_data.get('อปท.', temple_data.get('ตำบล', '')),
    }
    
    context = {
        'temple': temple,
        'api_key': api_key,
        'temple_lat': temple['lat'],
        'temple_lng': temple['lng'],
    }
    
    return render(request, 'temple_detail_map.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Add user to the 'sisaket login' group
            group, created = Group.objects.get_or_create(name='sisaket login')
            user.groups.add(group)
            
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})