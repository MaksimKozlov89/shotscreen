from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, AddScreenshotForm, UploadForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . import models
from django.contrib.sites.shortcuts import get_current_site


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('account', args=['all']))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'main/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'main/register.html', {'user_form': user_form})


@login_required()
def add_screenshot(request):
    if request.method == 'POST':
        form = AddScreenshotForm(request.POST, request.FILES)
        if form.is_valid():
            new_screenshot = form.save(commit=False)
            new_screenshot.author = request.user
            new_screenshot.save()
            return redirect(reverse('account', args=['all']))
    else:
        form = AddScreenshotForm()
    return render(request, 'main/add_screenshot.html', {'form': form})


@login_required()
def account(request, filter_='all'):
    my_screens = models.Screenshot.objects.filter(author=request.user)

    if filter_ == 'day':
        now = datetime.now() - timedelta(minutes=24 * 60)
        my_screens = my_screens.filter(created__gte=now)
    elif filter_ == 'week':
        now = datetime.now() - timedelta(minutes=24 * 60 * 7)
        my_screens = my_screens.filter(created__gte=now)
    elif filter_ == 'all':
        my_screens = my_screens
    domain_ = ''.join(['http://', get_current_site(request).domain])
    return render(request, 'main/account.html', {'screens': my_screens, 'link': domain_})


def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            new_screenshot = form.save(commit=False)
            new_screenshot.author = request.user
            new_screenshot.save()
            return HttpResponse('Done')
        else:
            return HttpResponse('Fail')
    else:
        form = UploadForm
    return render(request, 'main/upload.html', {'form': form})


def delete(request, id_screen):
    screen = models.Screenshot.objects.get(id=id_screen)
    screen.delete()
    return redirect(reverse('account', args=['all']))


def screen_detail(request, pk):
    screen = get_object_or_404(models.Screenshot, pk=pk)
    return render(request, 'main/screen_detail.html', context={'screen': screen})


def download(request):
    return render(request, 'main/download.html')






