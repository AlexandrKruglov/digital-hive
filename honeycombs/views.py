from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView

from honeycombs.forms import HoneycombsForm
from honeycombs.models import Honeycombs
from subscription.models import Subscription
from users.models import User


# Create your views here.
class HoneycombsPageVeiw(TemplateView):
    template_name = 'honeycombs/start.html'


class HoneycombsCreateView(CreateView):
    model = Honeycombs
    form_class = HoneycombsForm
    success_url = reverse_lazy('honeycombs:lk')

    def form_valid(self, form):
        honeycombs_form = form.save()
        user = self.request.user
        honeycombs_form.owner = user
        honeycombs_form.save()
        return super().form_valid(form)


class HoneycombsUpdateView(UpdateView):
    model = Honeycombs
    form_class = HoneycombsForm
    success_url = reverse_lazy('honeycombs:lk')


class HoneycombsListView(ListView):
    model = Honeycombs
    template_name = 'honeycombs/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['honeycombs'] = Honeycombs.objects.all().order_by('?')[:3]
        return context_data

class HoneycombsTopicListView(ListView):
    model = Honeycombs


    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return Honeycombs.objects.filter(topic=self.kwargs.get('topic'))
    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     honeycombs = Honeycombs.objects.all()
    #     honeycombs = honeycombs.filter(topic=self.kwargs.get('topic'))
    #     print(f'22{kwargs}')
    #     context['honeycombs'] = honeycombs
    #     return context


class ProfileListView(ListView):
    model = Honeycombs
    template_name = 'honeycombs/lk.html'


class HoneycombsDetailView(DetailView):
    model = Honeycombs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        avtor = User.objects.all()
        print(self.object.owner)
        avtor = avtor.filter(phone=self.object.owner)
        subscription = Subscription.objects.all()
        print(avtor)
        user = self.request.user
        subscription = subscription.filter(user=user, subscribe_to_user__in=avtor)
        print(subscription)
        context['subscription'] = subscription.first()
        context['avtor'] = avtor
        print(context)
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Honeycombs
    success_url = reverse_lazy('honeycombs:lk')
