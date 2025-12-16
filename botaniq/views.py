from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from dashboard.forms import CustomUserCreationForm
import os
from django.core.management import call_command
from io import StringIO
from django.http import HttpResponseForbidden


def home(request):
    """Home page for BotanIQ"""
    return render(request, 'home.html')


def custom_login(request):
    """Custom login view that redirects based on user type"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                # Redirect based on user type
                if user.is_staff:
                    return redirect('dashboard:admin_dashboard')
                else:
                    return redirect('dashboard:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def run_seed(request, token: str):
    """Protected one-off endpoint to run the seed_plants management command.

    Usage: set an environment variable SEED_TOKEN on the production host, then
    call /internal/seed/<token>/ to trigger seeding. This is temporary and
    should be removed after use.
    """
    secret = os.environ.get('SEED_TOKEN')
    if not secret or token != secret:
        return HttpResponseForbidden('Forbidden')

    out = StringIO()
    call_command('seed_plants', stdout=out)
    return HttpResponse(out.getvalue(), content_type='text/plain')
