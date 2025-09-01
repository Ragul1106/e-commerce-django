from django.urls import path
from .views import ProductListView, ProductDetailView, add_to_cart, remove_from_cart, cart_view, checkout, signup_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/<int:pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name='remove-from-cart'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
     path('logout/', auth_views.LogoutView.as_view(next_page='product-list'), name='logout'),
]
