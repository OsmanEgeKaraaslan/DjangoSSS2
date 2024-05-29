from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.home,name="home"),
    path('toys',views.toys,name="toys"),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart',views.cart,name="cart"),
    path('accounts/profile/', views.user_profile, name='profile'),
    path('checkout', views.checkout, name='checkout'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('order-history/', views.order_history, name='order_history'),



]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)