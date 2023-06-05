from .models import Account

def get_user(request):
    user = Account.objects.get(id=request.user.id)
    return user