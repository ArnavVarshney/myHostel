from django.shortcuts import render

from authentication.models import User


def user_validation(request):
    try:
        id_token = request.COOKIES['user']
        id_token_role = User.objects.get(uid=id_token).role
        if id_token_role == 1:
            return {'user_uid': id_token, 'user_role': 'Student'}
        elif id_token_role == 2:
            return {'user_uid': id_token, 'user_role': 'Warden'}
        elif id_token_role == 3:
            return {'user_uid': id_token, 'user_role': 'School'}
    except KeyError:
        pass


def index(request):
    user_validation_dict = user_validation(request)
    if user_validation_dict is not None:
        return render(request, 'index.html', {'logged_in': True})
    return render(request, 'index.html')
