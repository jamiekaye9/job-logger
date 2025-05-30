from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from jobs.forms.forms import CustomUserCreationForm, JobApplicationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import JobApplication

def home(request):
    return render(request, 'home/home.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenicationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_username()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenicationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile/profile.html')

@login_required
def job_application_list(request):
    applications = JobApplication.objects.filter(user=request.user)
    return render(request, 'profile/job_application_list.html', {'applications': applications})

@login_required
def job_application_form(request):
    if request.method == 'POST':
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.user = request.user
            job_application.save()
            return redirect('job_application_list')
    else:
        form = JobApplicationForm()
    return render(request, 'profile/job_application_form.html', {'form': form})