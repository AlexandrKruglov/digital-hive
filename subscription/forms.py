from django.forms import ModelForm

from subscription.models import Payments, Subscription


class PaymentsForm(ModelForm):
    class Meta:
        model = Payments
        fields = ()


class SubscriptionsForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ()



