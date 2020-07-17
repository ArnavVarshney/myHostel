from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render

from announcements.forms import CreateAnnouncementForm
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


def create_announcement(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    user_role = user_validation_dict['user_role']
    if request.method == 'POST':
        form = CreateAnnouncementForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creation_user = User.objects.get(uid=user_uid)
            instance.save()
            all_users = User.objects.filter(role=1)
            student_emails = []
            for user in all_users:
                student_emails.append(user.email)
            if student_emails:
                message = f"Hello,\n\nA new announcement was created by {instance.creation_user.first_name} " \
                          f"{instance.creation_user.last_name}\nMessage:\n{form.cleaned_data.get('message')}" \
                          f"\n\nThanks,\n\nYour myHostel team"
                send_mail(subject="New Announcement", message=message, recipient_list=student_emails,
                          from_email="myhostelgiis@gmail.com")
            return render(request, f'announcements/{user_role}/create_announcement.html',
                          {'form': form, 'status': 1, 'msg': 'Announcement created successfully'})
        return render(request, f'announcements/{user_role}/create_announcement.html', {'form': form})
    else:
        return render(request, f'announcements/{user_role}/create_announcement.html',
                      {'form': CreateAnnouncementForm()})
