

from subscription.models import Payments, Subscription
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm, PasswordChangeForm
from django import forms
from django.forms import ModelForm

# from catalog.form import StyleFormMixin
from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("phone", "nickname", "password1", "password2",)


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("phone", "nickname", "first_name", "last_name", "email", "avatar", "summ_subscription")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class UserPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ("old_password", "new_password1", "new_password2")


class CheckTokenForm(ModelForm):
    class Meta:
        model = User
        fields = ("token",)
