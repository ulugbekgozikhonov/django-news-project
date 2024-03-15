from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from accounts.models import Profile


# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data["username"], password=data["password"])
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Success")
                else:
                    return HttpResponse("Error")
            else:
                return HttpResponse("Login or Password Error")
    else:
        form = LoginForm()

        context = {
            'form': form
        }

        return render(request, 'registration/login.html', context)


def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'pages/user_profile.html', context=context)


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user': new_user
            }

            return render(request, 'account/register_done.html', context)

    user_form = UserRegistrationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'account/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'


class SignUpView2(View):
    @staticmethod
    def get(request):
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'account/register.html', context)

    @staticmethod
    def post(request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {
                'new_user': new_user
            }

            return render(request, 'account/register_done.html', context)


def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})


class EditUserView(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

    @staticmethod
    def post(request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('user_profile')
