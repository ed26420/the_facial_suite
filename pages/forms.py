from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm, 
    PasswordResetForm, 
    SetPasswordForm
)
from .models import UserProfile, Comment, TeamInquiry


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_control p-3', 
        'placeholder': 'Enter password',
        'style': 'background: #fff; height: 50px;',
        'autocomplete': 'new-password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_control p-3', 
        'placeholder': 'Confirm password',
        'style': 'background: #fff; height: 50px;',
        'autocomplete': 'new-password'
    }))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form_control p-3', 'placeholder': 'Enter email address', 'style': 'background: #fff; height: 50px;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"] # Use email as Django username
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'residential_address', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Enter phone number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form_control', 'type': 'date'}),
            'residential_address': forms.Textarea(attrs={'class': 'form_control p-3', 'placeholder': 'Enter residential address', 'rows': 3, 'style': 'background: #fff;'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form_control p-2', 'style': 'background: #fff; height: 50px;'}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_control'}),
            'email': forms.EmailInput(attrs={'class': 'form_control p-3'}),
            'first_name': forms.TextInput(attrs={'class': 'form_control'}),
            'last_name': forms.TextInput(attrs={'class': 'form_control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Prevents crash if username belongs to the current user
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken by another user.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Prevents crash if email belongs to the current user
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email address is already registered to another user.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone_number', 'date_of_birth', 'residential_address']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form_control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form_control', 'type': 'date'}),
            'residential_address': forms.Textarea(attrs={'class': 'form_control p-3', 'rows': 3}),
            'profile_picture': forms.FileInput(attrs={'class': 'form_control p-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Explicitly make profile fields optional so leaving them empty never causes a crash
        for field in ['phone_number', 'date_of_birth', 'residential_address', 'profile_picture']:
            if field in self.fields:
                self.fields[field].required = False


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form_control p-3', 
        'placeholder': 'Enter email or username',
        'style': 'background: #fff; height: 50px;',
        'autocomplete': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form_control p-3', 
        'placeholder': 'Enter password',
        'style': 'background: #fff; height: 50px;',
        'autocomplete': 'current-password'
    }))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form_control p-3', 
        'placeholder': 'Enter your email address',
        'style': 'background: #fff; height: 50px;',
        'autocomplete': 'email'
    }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form_control p-3', 
            'placeholder': 'Enter new password',
            'style': 'background: #fff; height: 50px;',
            'autocomplete': 'new-password'
        })
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={
            'class': 'form_control p-3', 
            'placeholder': 'Confirm new password',
            'style': 'background: #fff; height: 50px;',
            'autocomplete': 'new-password'
        })
    )

class TeamInquiryForm(forms.ModelForm):
    class Meta:
        model = TeamInquiry
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form_control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Mobile Number'}),
            'subject': forms.TextInput(attrs={'class': 'form_control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form_control', 'placeholder': 'Write message..', 'rows': 5}),
        }





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form_control', 
                'placeholder': 'Write your comment here...',
                'rows': 4,
                'required': True
            }),
        }