from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# 1. The Dashboard
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# 2. The Signup Logic (This was missing!)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})