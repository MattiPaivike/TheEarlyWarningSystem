from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.core.management import call_command

from .forms import UserRegisterForm, ProfileUpdateForm
from .models import CustomUser, Subscriptions, Profile
from main_app.models import Software, Version
from datetime import timezone, datetime

def register(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('app-home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            datas={}
            datas['email']=form.cleaned_data['email']
            datas['password1']=form.cleaned_data['password1']

            #We generate a random activation key
            activation_key = get_random_string(20, 'abcdefghijklmnopqrstuvwxyz1234567890(-_=+)')
            datas['activation_key']= activation_key
            call_command('email', 'activation', '', '', '', '', '', form.cleaned_data['email'], activation_key)
            form.save(datas) #Save the user and his profile
            email = form.cleaned_data.get('email')
            messages.success(request, f'Activation link sent to: {email}!')
            return redirect('email_sent', activation_key)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', locals())

def email_sent(request, key):
    profile = get_object_or_404(Profile, activation_key=key)
    if request.user.is_authenticated:
        return redirect('app-home')
    elif profile.user.is_active == False:
        return render(request, 'users/email_sent.html', locals())
    else:
       return redirect('app-home')


def activation(request, key):
    activation_expired = False
    already_active = False
    profile = get_object_or_404(Profile, activation_key=key)
    if request.user.is_authenticated:
        return redirect('app-home')
    elif profile.user.is_active == False:
            profile.user.is_active = True
            profile.user.save()
            email = str(profile.user.email)
            messages.success(request, f'{email} has been activated. You can now sign in!')
            return redirect('login')

    else:
        return redirect('app-home')

def resend_activation(request, key):
    profile = get_object_or_404(Profile, activation_key=key)
    if profile.user.is_active == False:
        if profile.sent_keys < 5:
            call_command('email', 'activation', '', '', '', '', '', str(profile.user.email), key)
            save_profile = profile.sent_keys = int(profile.sent_keys) + 1
            profile.save()
            messages.success(request, f'Activation link has been resent!')
            return render(request, 'users/email_sent.html', locals())
        else:
            messages.warning(request, f'You have done that too many times. Please contant the website administrator!')
            return redirect('app-home')
    else:
        return redirect('app-home')



@login_required
def profile(request):
    page = 'profile'
    context = {
        'apps': Version.objects.all(),
    }
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request=request)
        if form.is_valid():
            data = form.cleaned_data
            #loop through all user selected checkboxes
            for key in data:
                software_name = Software.objects.get(name=key)
                User_name = CustomUser.objects.get(email=str(request.user.email))
                #if user selected = True
                if data.get(key) == True:
                    if not User_name.subscriptions_set.filter(app_subscriptions=str(software_name)).exists():
                        save_subscription = Subscriptions(app_subscriptions=str(software_name), user=request.user)
                        save_subscription.save()
                elif data.get(key) == False:
                    if User_name.subscriptions_set.filter(app_subscriptions=str(software_name)).exists():
                        delete_subscription = User_name.subscriptions_set.get(app_subscriptions__iexact=str(software_name))
                        delete_subscription.delete()
            messages.success(request, f'User settings updated!')
            return redirect('app-home')
    else:
        form = ProfileUpdateForm(request=request)
    return render(request, 'users/profile.html', locals())

@login_required
def change_password(request):
    page = 'change_password'
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, f'User settings updated!')
            return redirect('app-home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', locals())

@login_required
def profile_delete(request):
    if request.method == 'POST':
        User_name = CustomUser.objects.get(email=str(request.user.email))
        User_name.delete()
        messages.success(request, f'{str(User_name)} has been deleted.')
        return redirect('app-home')
    return render(request, 'users/profile_delete.html')


def login_view(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('app-home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', locals())
