from django.conf import settings
from .models import SystemSettings,Role

def system_settings(request):
    try:
        system_settings = SystemSettings.objects.first()  # Fetch your SystemSettings object
        # Fetch single role objects instead of QuerySet
        user_role2 = Role.objects.filter(id=2).first()
        user_role3 = Role.objects.filter(id=3).first()  # Fetch the role with ID 3
        # Initialize URLs to None
        fav_icon_url = None
        footer_logo_url = None
        header_logo_url = None

        if system_settings:
            # Update with the correct fields from SystemSettings
            if system_settings.fav_icon:
                fav_icon_url = settings.MEDIA_URL + system_settings.fav_icon
            if system_settings.footer_logo:
                footer_logo_url = settings.MEDIA_URL + system_settings.footer_logo
            if system_settings.header_logo:
                header_logo_url = settings.MEDIA_URL + system_settings.header_logo

    except SystemSettings.DoesNotExist:
        system_settings = None

    return {
        'system_settings': system_settings,
        'user_role2': user_role2,
        'user_role3': user_role3,
        'fav_icon': fav_icon_url,
        'footer_logo': footer_logo_url,
        'header_logo': header_logo_url,
    }
