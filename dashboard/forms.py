from django import forms

from authentication.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'my_giis_id', 'phone', 'role']

    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.CharField(label='Email', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    my_giis_id = forms.CharField(label='myGIIS ID', required=False)
    phone = forms.CharField(label='Phone', required=False)
    role = forms.IntegerField(label='Role', required=False,
                              widget=forms.Select(attrs={'readonly': 'readonly'},
                                                  choices=((1, 'Student'), (2, 'Warden'), (3, 'School'))))

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        profile_picture_clear = self.data.get('profile_picture-clear')
        email = self.data.get('email')
        if not profile_picture and profile_picture_clear == 'on':
            return ''
        elif profile_picture is None:
            return User.objects.get(email=email).profile_picture
        return profile_picture
