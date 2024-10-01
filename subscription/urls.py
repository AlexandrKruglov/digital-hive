from django.urls import path

from subscription.apps import SubscriptionConfig
from subscription.views import PaymentsCreateView, SubscriptionsCreate, SubscriptionsListView, SubscriptionDeleteView

app_name = SubscriptionConfig.name

urlpatterns = [
    path('subscriptions/create/<int:pk>/', SubscriptionsCreate.as_view(), name='subscriptions_create'),
    path('subscription_list/', SubscriptionsListView.as_view(), name='subscription_list'),
    path('subscription_delete/<int:pk>/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('payments_create/<int:pk>/', PaymentsCreateView.as_view(), name='payments_create'),
]
