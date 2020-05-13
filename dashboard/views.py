from django.shortcuts import render, redirect

from authentication.models import UserProfile
from dashboard.forms import ProfileForm


def user_validation(request):
    try:
        id_token = request.COOKIES['user']
        id_token_role = UserProfile.objects.get(uid=id_token).role
        if id_token_role == 1:
            return {'user_uid': id_token, 'user_role': 'Student'}
        elif id_token_role == 2:
            return {'user_uid': id_token, 'user_role': 'Warden'}
        elif id_token_role == 3:
            return {'user_uid': id_token, 'user_role': 'School'}
    except KeyError:
        return redirect('/authentication/login_session/')


def dashboard(request):
    user_validation_dict = user_validation(request)
    user_role = user_validation_dict['user_role']
    return render(request, f'dashboard/{user_role}/dashboard.html')


def profile(request):
    user_validation_dict = user_validation(request)
    user_role = user_validation_dict.get('user_role')
    user_uid = user_validation_dict['user_uid']
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            UserProfile.objects.filter(uid=user_uid).update(**form.cleaned_data)
    user_profile_object = UserProfile.objects.get(uid=user_uid)
    data = {'first_name': user_profile_object.first_name, 'last_name': user_profile_object.last_name,
            'role': user_profile_object.role, 'email': user_profile_object.email,
            'my_giis_id': user_profile_object.my_giis_id, 'phone': user_profile_object.phone,
            'profile_picture': user_profile_object.profile_picture}
    form = ProfileForm(initial=data)
    return render(request, f'dashboard/{user_role}/profile.html', {'form': form})
