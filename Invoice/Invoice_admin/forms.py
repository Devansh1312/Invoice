from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *
import re

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        
        # Minimum length validation
        if len(new_password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        # Check for at least one digit
        if not re.search(r'\d', new_password1):
            raise forms.ValidationError("Password must contain at least one number.")
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', new_password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', new_password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        return new_password2

class LoginForm(forms.Form):
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Phone", "class": "form-control"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise forms.ValidationError('Phone is required')
        return phone


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password check", "class": "form-control"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserUpdateProfileForm(forms.ModelForm):
    username_display = forms.CharField(label="Username", required=False, disabled=True)
    email_display = forms.CharField(label="Email", required=False, disabled=True)
    phone_display = forms.CharField(label="Phone", required=False, disabled=True)

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

        # Set the display fields as plain text (disabled)
        if instance:
            self.fields["username_display"].initial = instance.username
            self.fields["email_display"].initial = instance.email
            self.fields["phone_display"].initial = instance.phone

