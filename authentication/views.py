from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from authentication.forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
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


def add_users(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            User.objects.create(**form.cleaned_data).save()
            User.objects.get(email=form.cleaned_data['email']).send_verification_email(request.get_host(),
                                                                                       request.scheme)
            return render(request, f'authentication/{user_role}/add_users.html', {'form': form, 'status': 1,
                                                                                  'msg': 'Registered successfully! A verification '
                                                                                         'email has been sent to the registered '
                                                                                         'email ID'})
        return render(request, f'authentication/{user_role}/add_users.html', {'form': form})
    else:
        return render(request, f'authentication/{user_role}/add_users.html', {'form': RegistrationForm()})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            uid = User.objects.get(email=email).uid
            response = render(request, 'authentication/redirect_login.html')
            response.set_cookie('user', uid)
            return response
        return render(request, 'authentication/login.html', {'form': form})
    else:
        return render(request, 'authentication/login.html', {'form': LoginForm()})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User.objects.get(email=email).send_forgot_password_email(request.get_host(), request.scheme)
            return render(request, 'authentication/forgot_password.html',
                          {'form': form, 'status': 1, 'msg': 'Mail sent successfully!'})
        return render(request, 'authentication/forgot_password.html', {'form': form})
    else:
        return render(request, 'authentication/forgot_password.html', {'form': ForgotPasswordForm()})


def verify_email(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        try:
            if User.objects.filter(uid=uid).exists():
                User.objects.get(uid=uid).verify_email()
                return render(request, 'authentication/verify_email.html')
        except:
            pass


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            uid = request.POST.get('uid')
            password = form.cleaned_data['password']
            try:
                User.objects.get(uid=uid).reset_password(password)
            except:
                pass
            return redirect('login')
        return render(request, 'authentication/reset_password.html', {'form': form})
    else:
        uid = request.GET.get('uid')
        try:
            email = User.objects.get(uid=uid).email
            return render(request, 'authentication/reset_password.html', {'form': ResetPasswordForm(), 'email': email})
        except:
            pass


def logout(request):
    response = render(request, 'index.html', {'logout': 1})
    response.delete_cookie('user')
    return response


def redirect_login(request):
    return render(request, 'authentication/redirect_login.html')


def view_all_users(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    user_uid = user_validation_dict['user_uid']
    all_objects = User.objects.all().exclude(uid=user_uid)
    if all_objects:
        return render(request, f'authentication/{user_role}/view_all_users.html',
                      {'all_objects': all_objects, 'uid': user_uid})
    return render(request, f'authentication/{user_role}/view_all_users.html')


def disable_user(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    User.objects.get(uid=uid).disable_user()
    return redirect('view_all_users')


def delete_user(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    User.objects.get(uid=uid).delete_user()
    return redirect('view_all_users')


def enable_user(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    User.objects.get(uid=uid).enable_user()
    return redirect('view_all_users')
