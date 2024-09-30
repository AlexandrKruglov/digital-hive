from django.urls import path

from honeycombs.apps import HoneycombsConfig
from honeycombs.views import HoneycombsPageVeiw, HoneycombsCreateView, HoneycombsUpdateView, HoneycombsListView, \
    ProfileListView, HoneycombsDetailView, ProductDeleteView, HoneycombsTopicListView

app_name = HoneycombsConfig.name

urlpatterns = [
    path('', HoneycombsPageVeiw.as_view(), name='start'),
    path('list/', HoneycombsListView.as_view(), name='list'),
    path('list_topic/<str:pk>', HoneycombsTopicListView.as_view(), name='list_topic'),
    path('create/', HoneycombsCreateView.as_view(), name='create'),
    path('update/<int:pk>/', HoneycombsUpdateView.as_view(), name='update'),
    path('home', HoneycombsListView.as_view(), name='home'),
    path('lk', ProfileListView.as_view(), name='lk'),
    path('honeycombs/<int:pk>/', HoneycombsDetailView.as_view(), name='honeycombs_detail'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    ]
