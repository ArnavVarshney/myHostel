from django.shortcuts import render, redirect

from authentication.forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from authentication.models import UserProfile


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            UserProfile.objects.create(**form.cleaned_data)
            UserProfile.objects.get(**form.cleaned_data).send_verification_email(request.scheme, request.get_host())
            return render(request, 'authentication/register.html', {'form': form, 'status': 1,
                                                                    'msg': 'Registered successfully! A verification '
                                                                           'email has been sent to the registered '
                                                                           'email ID'})
        return render(request, 'authentication/register.html', {'form': form})
    else:
        return render(request, 'authentication/register.html', {'form': RegistrationForm()})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('dashboard')
        return render(request, 'authentication/login.html', {'form': form})
    else:
        return render(request, 'authentication/login.html', {'form': LoginForm()})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            UserProfile.objects.get(email=email).send_forgot_password_email(request.scheme, request.get_host())
            return render(request, 'authentication/forgot_password.html',
                          {'form': form, 'status': 1, 'msg': 'Mail sent successfully!'})
        return render(request, 'authentication/forgot_password.html', {'form': form})
    else:
        return render(request, 'authentication/forgot_password.html', {'form': ForgotPasswordForm()})


def verify_email(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        try:
            if UserProfile.objects.filter(uid=uid).exists():
                UserProfile.objects.get(uid=uid).verify_email()
                return render(request, 'authentication/verify_email.html', {'status': 1})
        except:
            return render(request, 'authentication/verify_email.html', {'status': 2})
    return render(request, 'authentication/verify_email.html', {'status': 2})


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            uid = request.POST.get('uid')
            password = form.cleaned_data['password']
            try:
                UserProfile.objects.get(uid=uid).reset_password(password)
            except:
                return render(request, 'authentication/reset_password.html',
                              {'form': form, 'status': 2, 'msg': 'Invalid request'})
            return redirect('login')
        return render(request, 'authentication/reset_password.html', {'form': form})
    else:
        uid = request.GET.get('uid')
        try:
            email = UserProfile.objects.get(uid=uid).email
        except:
            return render(request, 'authentication/reset_password.html',
                          {'form': ResetPasswordForm(), 'status': 2, 'msg': 'Invalid request'})
        return render(request, 'authentication/reset_password.html', {'form': ResetPasswordForm(), 'email': email})


def logout(request):
    return None
