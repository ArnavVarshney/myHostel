from django import forms

from announcements.models import Announcement


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['message']

    message = forms.Textarea()
