from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from jobs.models import JobApplication, Stage


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['company_name', 'job_title', 'salary', 'location', 'date_applied', 'status']
        widgets = {
            'date_applied': forms.DateInput(attrs={'type': 'date'}),
        }

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage_name', 'stage_date_time', 'status']
        widgets = {
            'stage_date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }