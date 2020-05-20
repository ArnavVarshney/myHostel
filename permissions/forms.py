from django import forms

from permissions.models import Permission


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['request_name', 'request_message']

    request_name = forms.CharField(label='Request Name', required=True)
    request_message = forms.CharField(label='Request Message', required=True, widget=forms.Textarea)
