from django.urls import path
from . import views
from .views import PaymentView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.menu_list, name='menu'),
    path('menu/<int:id>/', views.menu_detail, name='menu_detail'),
    path('add-to-cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:menu_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
     path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/success/', TemplateView.as_view(template_name='payment_success.html'), name='payment_success'),
    path('payment/error/', TemplateView.as_view(template_name='payment_error.html'), name='payment_error'),
]