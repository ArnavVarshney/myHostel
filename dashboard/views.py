from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from authentication.models import User
from dashboard.forms import ProfileForm


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
        raise PermissionDenied


def dashboard(request):
    user_validation_dict = user_validation(request)
    user_role = user_validation_dict['user_role']
    return render(request, f'dashboard/{user_role}/dashboard.html')


def profile(request):
    user_validation_dict = user_validation(request)
    user_role = user_validation_dict.get('user_role')
    user_uid = user_validation_dict['user_uid']
    params = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(uid=user_uid)
            user.profile_picture = form.cleaned_data['profile_picture']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.my_giis_id = form.cleaned_data['my_giis_id']
            user.phone = form.cleaned_data['phone']
            user.save()
            params['status'] = 1
            params['msg'] = 'Profile updated'
    user_profile_object = User.objects.get(uid=user_uid)
    data = {'first_name': user_profile_object.first_name, 'last_name': user_profile_object.last_name,
            'role': user_profile_object.role, 'email': user_profile_object.email,
            'my_giis_id': user_profile_object.my_giis_id, 'phone': user_profile_object.phone,
            'profile_picture': user_profile_object.profile_picture}
    form = ProfileForm(initial=data)
    params['form'] = form
    return render(request, f'dashboard/{user_role}/profile.html', params)
