
from django.urls import path
from interview.order.views import OrderListCreateView, \
    OrderTagListCreateView, DeactivateOrderView, \
        OrderFilterDateView, OrderTagCreateView, TagOrderCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('<int:id>/tags/', OrderTagCreateView.as_view(), name='order-tag-list'),
    path('tags/<int:id>',TagOrderCreateView.as_view(),name='tag-order-list'),
    path('deactivate/<int:id>/', DeactivateOrderView.as_view(), name='deactivate-order'),
    path('date/<str:start_date>&<str:embargo_date>',OrderFilterDateView.as_view(), name = 'date-range-order')
]