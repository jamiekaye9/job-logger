from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from jobs.forms.forms import CustomUserCreationForm

def home(request):
    return render(request, 'home/home.html')

def profile(request):
    return render(request, 'profile/profile.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})