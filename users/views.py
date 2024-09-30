import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, UserPasswordChangeForm, CheckTokenForm
from users.models import User
from users.services import send_sms


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm

    template_name = 'users/register.html'
    success_url = reverse_lazy('users:token')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        phone = user.phone
        token = ''
        for x in range(4):
            token = token + str(random.randint(0, 9))
        user.token = token
        user.save()
        # send_sms(phone, token)   # реальная отпрака смс
        return redirect('users:token', token)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('honeycombs:lk')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


class CheckTokenView(View):
    model = User
    form_class = CheckTokenForm
    template_name = 'users/token.html'
    success_url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        print(f'?11{kwargs}')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        token = kwargs.get('token')
        form_token = request.POST.get('token')
        if form_token != token:
            return redirect('users:token', token=token)
        user = get_object_or_404(User, token=token)
        user.is_active = True
        user.save()
        return redirect('users:login')
