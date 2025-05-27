import web.settings as sett

def media_admin(request):
    context = {
        'media_url':sett.MEDIA_URL
    }


    return context