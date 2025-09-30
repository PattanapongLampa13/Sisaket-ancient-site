from django.conf import settings

def global_settings(request):
    duration_seconds = getattr(settings, 'CUSTOM_SESSION_DURATION_SECONDS', 3600)
    return {
        'CUSTOM_SESSION_DURATION_MS': duration_seconds * 1000,
        'api_key': getattr(settings, 'GOOGLE_MAPS_API_KEY', ''),
    }
