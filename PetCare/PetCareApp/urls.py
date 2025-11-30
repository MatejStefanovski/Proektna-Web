from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('veterinari/', views.veterinari, name='veterinari'),
    path('oprema/', views.oprema, name='oprema'),
    path('hotel/', views.hotel, name='hotel'),
    path('igracki/', views.igracki, name='igracki'),
    path('milenicinja/', views.milenicinja, name='milenicinja'),
    path('hrana/', views.hrana, name='hrana'),
    path('nega/', views.nega, name='nega'),
    path('dresiranje/', views.dresiranje, name='dresiranje'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-checkout/', views.process_checkout, name='process_checkout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-all-from-cart/<int:product_id>/', views.remove_all_from_cart, name='remove_all_from_cart'),
] 