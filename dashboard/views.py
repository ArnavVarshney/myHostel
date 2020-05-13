from django.shortcuts import render, redirect


def dashboard(request):
    try:
        id_token = request.COOKIES['user']
    except KeyError:
        return redirect('/authentication/login_session/')
    return render(request, 'dashboard/Student/dashboard.html')
