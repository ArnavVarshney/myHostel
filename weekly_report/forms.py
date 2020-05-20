from django import forms

from weekly_report.models import WeeklyReport, Report


class CreateReportForm(forms.ModelForm):
    class Meta:
        model = WeeklyReport
        fields = ['date']

    date = forms.DateField(widget=forms.SelectDateWidget())


class FillReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report']

    report = forms.Textarea()
