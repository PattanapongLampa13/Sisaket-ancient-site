import os
from django.shortcuts import render

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