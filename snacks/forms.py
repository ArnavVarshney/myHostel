from django import forms

from snacks.models import Snack, Bill


class SnacksForm(forms.ModelForm):
    class Meta:
        model = Snack
        fields = ['date', 'notify_students']

    date = forms.DateField(widget=forms.SelectDateWidget())


class BillUploadForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['bill', 'amount']
