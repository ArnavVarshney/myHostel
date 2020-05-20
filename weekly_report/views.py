from datetime import timedelta

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from authentication.models import User
from weekly_report.forms import CreateReportForm, FillReportForm
from weekly_report.models import WeeklyReport, Report


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


def fill_report(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Hostel', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    user_role = user_validation_dict['user_role']
    if request.method == 'POST':
        form = FillReportForm(request.POST)
        if form.is_valid():
            weekly_report_uid = request.POST.get('weekly_report_uid')
            try:
                Report.objects.get(weekly_report_uid=weekly_report_uid, creation_user_id=user_uid)
                report_object = Report.objects.filter(weekly_report_uid=weekly_report_uid, creation_user_id=user_uid)
                report_object.update(**form.cleaned_data)
                return redirect('view_pending_reports')
            except:
                instance = form.save(commit=False)
                instance.creation_user = User.objects.get(uid=user_uid)
                instance.weekly_report_uid = WeeklyReport.objects.get(uid=weekly_report_uid)
                instance.save()
                return redirect('view_pending_reports')
        return render(request, f'weekly_report/{user_role}/fill_report.html', {'form': form})
    weekly_report_uid = request.GET.get('uid')
    weekly_report_object = WeeklyReport.objects.get(uid=weekly_report_uid)
    try:
        report_object = Report.objects.get(weekly_report_uid=weekly_report_uid, creation_user_id=user_uid)
        data = {'report': report_object.report}
        form = FillReportForm(initial=data)
        return render(request, f'weekly_report/{user_role}/fill_report.html',
                      {'form': form, 'weekly_report_uid': weekly_report_uid,
                       'object': weekly_report_object})
    except:
        pass
    return render(request, f'weekly_report/{user_role}/fill_report.html',
                  {'form': FillReportForm(), 'weekly_report_uid': weekly_report_uid, 'object': weekly_report_object})


def create_report(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Warden', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    if request.method == 'POST':
        form = CreateReportForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            for days in range(0, 7):
                date_mod = (date + timedelta(days=days)).strftime('%Y-%m-%d')
                form_new = CreateReportForm(data={'date': date_mod})
                instance = form_new.save(commit=False)
                instance.creation_user = User.objects.get(uid=user_uid)
                instance.save()
            return render(request, f'weekly_report/Warden/create_report.html',
                          {'form': form, 'status': 1, 'msg': 'Report week created successfully'})
        return render(request, f'weekly_report/Warden/create_report.html', {'form': form})
    else:
        return render(request, f'weekly_report/Warden/create_report.html', {'form': CreateReportForm()})


def view_all_previous_reports(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    all_objects = WeeklyReport.objects.all()
    if all_objects:
        return render(request, f'weekly_report/{user_role}/view_all_previous_reports.html',
                      {'all_objects': all_objects})
    return render(request, f'weekly_report/{user_role}/view_all_previous_reports.html')


def view_previous_reports(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Hostel', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    user_role = user_validation_dict['user_role']
    weekly_report_objects = WeeklyReport.objects.all()
    submitted_reports = []
    for report in weekly_report_objects:
        if Report.objects.filter(weekly_report_uid=report.uid, creation_user_id=user_uid).exists():
            submitted_reports.append(report)
    if len(submitted_reports) != 0:
        return render(request, f'weekly_report/{user_role}/view_previous_reports.html',
                      {'all_objects': submitted_reports})


def view_pending_reports(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Hostel', user_validation_dict)
    user_uid = user_validation_dict['user_uid']
    user_role = user_validation_dict['user_role']
    all_reports = WeeklyReport.objects.all()
    pending_reports = []
    for report in all_reports:
        if not Report.objects.filter(weekly_report_uid=report.uid, creation_user_id=user_uid).exists():
            pending_reports.append(report)
    if len(pending_reports) != 0:
        return render(request, f'weekly_report/{user_role}/view_pending_reports.html',
                      {'pending_reports_objects': pending_reports})
    return render(request, f'weekly_report/{user_role}/view_pending_reports.html')


def view_report_info(request):
    user_validation_dict = user_validation(request)
    user_role_validation(request, 'Admin', user_validation_dict)
    user_role = user_validation_dict['user_role']
    uid = request.GET.get('uid')
    weekly_report_object = WeeklyReport.objects.get(uid=uid)
    try:
        report_objects = Report.objects.filter(weekly_report_uid=uid)
        return render(request, f'weekly_report/{user_role}/view_report_info.html',
                      {'weekly_report_object': weekly_report_object, 'report_objects': report_objects})
    except:
        pass
    return render(request, f'weekly_report/{user_role}/view_report_info.html',
                  {'weekly_report_object': weekly_report_object})
