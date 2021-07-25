from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from authentication.models import User
from snacks.forms import SnacksForm, BillUploadForm
from snacks.models import Snack, Bill


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


def view_all_previous_snacks(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    all_objects = Snack.objects.all()
    if all_objects:
        return render(request, f'snacks/{user_role}/view_all_previous_snacks.html',
                      {'all_objects': all_objects})
    return render(request, f'snacks/{user_role}/view_all_previous_snacks.html')


def create_snacks(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    if request.method == 'POST':
        form = SnacksForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.creation_user = User.objects.get(uid=user_validation_dict['user_uid'])
            instance.save()
            try:
                if form.data['notify_students']:
                    all_users = User.objects.filter(role=1)
                    student_emails = []
                    for user in all_users:
                        student_emails.append(user.email)
                    if student_emails:
                        message = f"Hello,\n\nA new snacks entry for {instance.date} was created by " \
                                  f"{instance.creation_user.first_name} " \
                                  f"{instance.creation_user.last_name}\n\nThanks,\n\nYour myHostel team"
                        send_mail(subject="New Snacks Entry", message=message, recipient_list=student_emails,
                                  from_email="myhostelgiis@gmail.com")
            except:
                pass
            return render(request, f'snacks/{user_role}/create_snacks.html',
                          {'form': form, 'status': 1, 'msg': 'Snacks entry created successfully'})
        return render(request, f'snacks/{user_role}/create_snacks.html', {'form': form})
    else:
        return render(request, f'snacks/{user_role}/create_snacks.html', {'form': SnacksForm()})


def upload_bills(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Student', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    if request.method == 'POST':
        form = BillUploadForm(request.POST, request.FILES)
        if form.is_valid():
            snack_uid = request.POST.get('snack_uid')
            instance = form.save(commit=False)
            instance.creation_user = User.objects.get(uid=user_uid)
            instance.snack_uid = Snack.objects.get(uid=snack_uid)
            instance.save()
            return render(request, 'snacks/Student/upload_bills.html',
                          {'form': form, 'status': 1, 'msg': 'Bill uploaded successfully'})
        return render(request, 'snacks/Student/upload_bills.html', {'form': form})
    snack_uid = request.GET.get('uid')
    return render(request, 'snacks/Student/upload_bills.html', {'form': BillUploadForm(), 'snack_uid': snack_uid})


def view_snacks_info(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    uid = request.GET.get('uid')
    snack_object = Snack.objects.get(uid=uid)
    try:
        bill_objects = Bill.objects.filter(snack_uid_id=uid)
        total_amount = 0.0
        for bill in bill_objects:
            total_amount += float(bill.amount)
        return render(request, f'snacks/{user_role}/view_snacks_info.html',
                      {'snack_object': snack_object, 'bill_objects': bill_objects, 'total_amount': total_amount})
    except:
        pass
    return render(request, f'snacks/{user_role}/view_snacks_info.html', {'snack_object': snack_object})


def view_pending_snacks(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Student', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    all_snacks = Snack.objects.all()
    pending_snacks = []
    for snack in all_snacks:
        if not Bill.objects.filter(snack_uid_id=snack.uid, creation_user_id=user_uid).exists():
            pending_snacks.append(snack)
    if len(pending_snacks) != 0:
        return render(request, 'snacks/Student/view_pending_snacks.html', {'pending_snacks_objects': pending_snacks})
    return render(request, 'snacks/Student/view_pending_snacks.html')


def remove_snacks_bill(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    uid = request.GET.get('uid')
    snack_user_uid = request.GET.get('user')
    Bill.objects.get(snack_uid_id=uid, creation_user_id=snack_user_uid).delete()
    return redirect('/snacks/view_snacks_info' + '/?uid=' + uid)
