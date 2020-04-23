from django.shortcuts import render, redirect
from .forms import UserCreationForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            # username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            # messages.success(request,'félicitation {} L inscription sest terminée avec succès'.format(username))
            messages.success(request, f'The user {new_user} was added successfully. You may edit it again below.')
            return redirect('login')
        else:
            messages.warning(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'user/register.html', {

        'title': 'inscrire',
        'form': form,
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')

        else:
            messages.warning(
                request, 'Il y a une erreur ')
    return render(request, 'user/login.html', {
        'title': 'se connecter',
    })


def logout_user(request):
    logout(request)
    return render(request, 'user/logout.html', {
        'title': 'déconnecter',
    })


@login_required(login_url='login')
def profile(request):
    posts = Post.objects.filter(author=request.user)
    post_list = Post.objects.filter(author=request.user)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_page)
    return render(request, 'user/profile.html', {
        'title': 'profile',
        'posts': posts,
        'page': page,
        'post_list': post_list,

    })


@login_required(login_url='login')
def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(
                request, 'success')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'modifier le profilي',
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'user/update.html', context)
