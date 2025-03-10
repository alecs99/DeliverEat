"""DeliverEat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from delivereatproj.views import (
    index,
    RegisterView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserProfileUpdateView,
    RestaurantDetail,
    CartDetail,
    ProductDeleteView,
    ProductAddView,
    OrderView, CheckoutView, OrdersListView, FeedbackView, FeedbackDetailsView)

urlpatterns = [
    path('', index, name='restaurants_list'),
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userprofile', UserProfileView.as_view(), name='user_profile'),
    path('userprofile/<int:pk>/edit', UserProfileUpdateView.as_view(), name='user_profile_edit'),
    path('restaurant/<int:pk>', RestaurantDetail.as_view(), name='restaurant_detail'),
    path('cart/<int:pk>', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:pk_product>', ProductAddView.as_view(), name='add_to_cart'),
    path('delete/<int:pk_product>', ProductDeleteView.as_view(), name='delete_product'),
    path('checkout', CheckoutView.as_view(), name="checkout"),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('order/<int:pk>/feedback', FeedbackView.as_view(), name='feedback'),
    path('order/<int:pk>/feedback_form', FeedbackView.as_view(), name='feedback_form'),
    path('order/<int:pk_order>/view_feedback', FeedbackDetailsView.as_view(), name='view_feedback'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
