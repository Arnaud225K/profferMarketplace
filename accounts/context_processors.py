from .models import UserProfile


def get_user(request):
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except:
        userprofile = None
    return dict(userprofile=userprofile)