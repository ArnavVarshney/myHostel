from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from authentication.models import User
from permissions.forms import PermissionsForm
from permissions.models import Permission


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


def user_role_validation(request, group, user_validation_dict):
    user_role = user_validation_dict['user_role']
    if group == 'Student':
        if user_role == 'School' or user_role == 'Warden':
            raise PermissionDenied
    elif group == 'Warden':
        if user_role == 'School' or user_role == 'Student':
            raise PermissionDenied
    elif group == 'Admin':
        if user_role == 'Student':
            raise PermissionDenied
    elif group == 'Hostel':
        if user_role == 'School':
            raise PermissionDenied


def new_request(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Student', user_validation_dict)
    if request.method == 'POST':
        form = PermissionsForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creation_user = User.objects.get(uid=user_validation_dict['user_uid'])
            instance.save()
            return render(request, 'permissions/Student/new_request.html',
                          {'form': form, 'status': 1, 'msg': 'Entry created successfully'})
        return render(request, 'permissions/Student/new_request.html', {'form': form})
    return render(request, 'permissions/Student/new_request.html', {'form': PermissionsForm()})


def view_previous_requests(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Student', user_validation_dict)
    all_objects = Permission.objects.filter(creation_user_id=user_validation_dict['user_uid'])
    if all_objects:
        return render(request, 'permissions/Student/view_previous_requests.html', {'all_objects': all_objects})
    return render(request, 'permissions/Student/view_previous_requests.html')


def view_all_previous_requests(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    all_objects = Permission.objects.all()
    if all_objects:
        return render(request, f'permissions/{user_role}/view_all_previous_requests.html',
                      {'all_objects': all_objects, 'role': user_role})
    return render(request, f'permissions/{user_role}/view_all_previous_requests.html')


def approve_request(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    Permission.objects.get(uid=uid).approve_request(role=user_validation_dict['user_role'])
    return redirect('review_requests')


def reject_request(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    Permission.objects.get(uid=uid).reject_request(role=user_validation_dict['user_role'])
    return redirect('review_requests')


def edit_request(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    Permission.objects.get(uid=uid).edit_request(role=user_validation_dict['user_role'])
    return redirect('review_requests')


def review_requests(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    if user_role == 'School':
        all_objects = Permission.objects.filter(status_school='Pending')
    elif user_role == 'Warden':
        all_objects = Permission.objects.filter(status_warden='Pending')
    if all_objects is not None:
        return render(request, f'permissions/{user_role}/review_requests.html', {'all_objects': all_objects})
    return render(request, f'permissions/{user_role}/review_requests.html')


def withdraw_request(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Student', user_validation_dict)
    uid = request.GET.get('uid')
    Permission.objects.get(uid=uid).withdraw_request()
    return redirect('view_previous_requests')
