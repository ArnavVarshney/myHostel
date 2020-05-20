from django.shortcuts import render, redirect

from authentication.forms import RegistrationForm, LoginForm, ResetPasswordForm, ForgotPasswordForm
from authentication.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            User.objects.create(**form.cleaned_data).save()
            User.objects.get(email=form.cleaned_data['email']).send_verification_email(request.get_host(),
                                                                                       request.scheme)
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
