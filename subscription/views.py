from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView

from subscription.forms import PaymentsForm, SubscriptionsForm
from subscription.models import Payments, Subscription
from subscription.services import create_price, create_session
from users.models import User


class PaymentsListView(ListView):
    model = Payments


class PaymentsCreateView(CreateView):
    model = Payments
    form_class = PaymentsForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_pay_data(self, pk):
        user = User.objects.all()
        user = user.filter(pk=pk).first()
        price = create_price(user.summ_subscription)
        session_id, link = create_session(price)
        return session_id, link

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        session_id, link = self.get_pay_data(pk)
        return HttpResponseRedirect(
            link)


class SubscriptionsCreate(CreateView):
    model = Subscription
    form_class = SubscriptionsForm

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avtor = User.objects.all()
        avtor = avtor.filter(pk=self.kwargs.get('pk'))
        context['avtor'] = avtor
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        g = User.objects.all()
        p = kwargs['pk']

        subscribe_to_user = g.filter(pk=p).first()
        subscription, created = Subscription.objects.get_or_create(user=user, subscribe_to_user=subscribe_to_user)
        if not created:
            subscription.delete()
        else:
            return redirect('subscription:payments_create', p)
        return redirect('subscription:payments_create', p)


class SubscriptionsListView(ListView):
    model = Subscription


class SubscriptionDeleteView(DeleteView):
    model = Subscription
    success_url = reverse_lazy('subscription:subscription_list')
