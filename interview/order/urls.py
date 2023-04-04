
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, DeactivateOrderView, OrderFilterDateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('deactivate/<int:id>/', DeactivateOrderView.as_view(), name='deactivate-order'),
    path('date/<str:start_date>&<str:embargo_date>',OrderFilterDateView.as_view(), name = 'date-range-order')
]