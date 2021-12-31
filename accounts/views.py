from django import views
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .models import TwitterUser, Follow

class RegisterUser(views.View):
    def get(self, request):
        user_form = UserForm()
        template_name = 'accounts/register.html'
        context = {
            'form': user_form
        }
        return render(request, template_name, context)
    def post(self, request):
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/login')
        else:
            template_name = 'accounts/register.html'
            context = {
                'form': user_form
            }
            return render(request, template_name, context)

class LoginUser(views.View):
    def get(self, request):
        form = AuthenticationForm()
        template_name = 'accounts/login.html'
        context = {
            'form': form
        }
        return render(request, template_name, context)
    def post(self, request):
        try:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, 'Inicio de sesión correcto')
                    return redirect('/users/')
                else:
                    messages.error(request, 'Credenciales inválidas')
                    template_name = 'accounts/login.html'
                    context = {
                        'form': form
                    }
                    return render(request, template_name, context)
            else:
                messages.error(request, 'El formulario es inválido')
                template_name = 'accounts/login.html'
                context = {
                    'form': form
                }
                return render(request, template_name, context)
        except Exception as e:
            print(e)
            messages.error(request, 'Error del servidor')
            template_name = 'accounts/login.html'
            context = {
                'form': form
            }
            return render(request, template_name, context)

def LogoutUser(request):
    logout(request)
    messages.success(request, 'Sesión cerrada con éxito')
    return redirect('/login/')


# USERS VIEWS
@login_required
def UserList(request):
    users = TwitterUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    for user in users:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()
        user.is_following = is_following
    template_name = 'users/list.html'
    context = {
        'users': users
    }
    return render(request, template_name, context)

def FollowUser(request):
    follower_id = request.POST['follower']
    followed_id = request.POST['followed']
    follower = TwitterUser.objects.get(id=follower_id)
    followed = TwitterUser.objects.get(id=followed_id)
    new_follow = Follow.objects.create(follower=follower, followed=followed)
    if new_follow:
        return redirect('/users/')
    else:
        messages.error(request, 'Algo falló al intentar seguir a ese usuario')
        return redirect('/users/')

def UnfollowUser(request):
    follower_id = request.POST['follower']
    followed_id = request.POST['followed']
    follower = TwitterUser.objects.get(id=follower_id)
    followed = TwitterUser.objects.get(id=followed_id)
    follow = Follow.objects.get(follower=follower, followed=followed)
    removed_follow = follow.delete()
    if removed_follow:
        return redirect('/users/')
    else:
        messages.error(request, 'Algo falló al intentar dejar de seguir a ese usuario')
        return redirect('/users/')