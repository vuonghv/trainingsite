from django import forms
from django.contrib.auth.models import User
from .models import TrainingUser


class UserForm(forms.ModelForm):
    """
    This form is used for sign user up
    """
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class TrainingUserForm(forms.ModelForm):
    """
    This form is used for displaying Sign training user up
    """
    class Meta:
        model = TrainingUser
        fields = ('website', 'github', 'twitter')


class UserProfileForm(forms.ModelForm):
    """
    This form is used for displaying User Profile
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class TrainingUserProfileForm(forms.ModelForm):
    """
    This form is used for displaying Training User Profile
    """
    # TODO: how to show date_udated with 'editable=False'
    date_updated = forms.DateTimeField(widget=forms.DateTimeInput())
    class Meta:
        model = TrainingUser
        fields = ('study_status', 'website', 'facebook',
                    'twitter', 'github', 'date_updated')
    
    class NewMeta:
        readonly = ('date_updated',)

