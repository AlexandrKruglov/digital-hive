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
    """Стартовая страница"""
    template_name = 'honeycombs/start.html'


class HoneycombsCreateView(CreateView):
    """Страница создания новой статьи"""
    model = Honeycombs
    form_class = HoneycombsForm
    success_url = reverse_lazy('honeycombs:lk')

    def form_valid(self, form):
        """Добавляем атора"""
        honeycombs_form = form.save()
        user = self.request.user
        honeycombs_form.owner = user
        honeycombs_form.save()
        return super().form_valid(form)


class HoneycombsUpdateView(UpdateView):
    """Страница редактирования статьи"""
    model = Honeycombs
    form_class = HoneycombsForm
    success_url = reverse_lazy('honeycombs:lk')


class HoneycombsListView(ListView):
    """Страница всех статей"""
    model = Honeycombs
    template_name = 'honeycombs/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['honeycombs'] = Honeycombs.objects.all().order_by('?')[:3]
        return context_data

class HoneycombsTopicListView(ListView):
    """Страница статей по теме"""
    model = Honeycombs


    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        """Фильтр статей по теме"""
        return Honeycombs.objects.filter(topic=self.kwargs.get('topic'))



class ProfileListView(ListView):
    """Список публикаций пользователя"""
    model = Honeycombs
    template_name = 'honeycombs/lk.html'


class HoneycombsDetailView(DetailView):
    """Просмотр конкретной статьи"""
    model = Honeycombs

    def get_context_data(self, **kwargs):
        """Выводим автора статьи и есть ли подписка"""
        context = super().get_context_data(**kwargs)
        avtor = User.objects.all()
        avtor = avtor.filter(phone=self.object.owner)
        subscription = Subscription.objects.all()
        user = self.request.user
        subscription = subscription.filter(user=user, subscribe_to_user__in=avtor)
        context['subscription'] = subscription.first()
        context['avtor'] = avtor
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление статьи"""
    model = Honeycombs
    success_url = reverse_lazy('honeycombs:lk')
