from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView

from subscription.forms import PaymentsForm, SubscriptionsForm
from subscription.models import Payments, Subscription
from subscription.services import create_price, create_session
from users.models import User




class PaymentsCreateView(CreateView):
    """Создание платежа"""
    model = Payments
    form_class = PaymentsForm

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_pay_data(self, pk):
        """Создание сесии и ссылки на оплате в страйп"""
        user = User.objects.all()
        user = user.filter(pk=pk).first()
        price = create_price(user.summ_subscription)
        session_id, link = create_session(price)
        return session_id, link

    def post(self, request, *args, **kwargs):
        """Переход по ссылке на оплату"""
        pk = kwargs['pk']
        session_id, link = self.get_pay_data(pk)
        return HttpResponseRedirect(
            link)


class SubscriptionsCreate(CreateView):
    """Создание подписки"""
    model = Subscription
    form_class = SubscriptionsForm

    def get(self, request, *args, **kwargs):

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Передаем в шаблон автора статьи"""
        context = super().get_context_data(**kwargs)
        avtor = User.objects.all()
        avtor = avtor.filter(pk=self.kwargs.get('pk'))
        context['avtor'] = avtor
        return context

    def post(self, request, *args, **kwargs):
        """Создание подписки пользователем на автора статьи"""
        user = self.request.user
        g = User.objects.all()
        p = kwargs['pk']

        subscribe_to_user = g.filter(pk=p).first()
        Subscription.objects.get_or_create(user=user, subscribe_to_user=subscribe_to_user)

        return redirect('subscription:payments_create', p)


class SubscriptionsListView(ListView):
    """Список подписок пользователя"""
    model = Subscription


class SubscriptionDeleteView(DeleteView):
    """Удаление подписки пользователя"""
    model = Subscription
    success_url = reverse_lazy('subscription:subscription_list')
