import binascii
import hashlib
import os

from django import forms

from authentication.models import User


def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwd_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwd_hash = binascii.hexlify(pwd_hash)
    return (salt + pwd_hash).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture', 'first_name', 'last_name', 'email', 'password', 'my_giis_id', 'phone', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() != 0:
            raise forms.ValidationError('User with the given email already exists')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return hash_password(password)

    profile_picture = forms.ImageField(label='Profile Picture', required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    email = forms.CharField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    my_giis_id = forms.CharField(label='myGIIS ID', required=False)
    phone = forms.CharField(label='Phone', required=False)
    role = forms.IntegerField(label='Role', required=False,
                              widget=forms.Select(choices=((1, 'Student'), (2, 'Warden'), (3, 'School'))))


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with the given email does not exist')
        elif not User.objects.get(email=email).enabled:
            raise forms.ValidationError('User has been disabled')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if User.objects.filter(email=email).exists():
            if not verify_password(User.objects.get(email=email).password, password):
                raise forms.ValidationError('Invalid email and password combination')
        return password

    email = forms.CharField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)


class ResetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)


class ForgotPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('User with the given email does not exist')
        return email

    email = forms.CharField(label='Email', required=True)
