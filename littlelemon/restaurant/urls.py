from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
  path('', views.index, name="index"),
  path('about/', views.about, name="about"),
  path('menu/', views.menu, name="menu"),
  path('menu/<int:pk>', views.menu_item, name="menu_item"),
  path('book/', views.book, name="book"),
  path('bookings/', views.bookings, name="bookings"),
  path('reservations/', views.reservations, name="reservations"),
  path('api-menu/', views.MenuItemsView.as_view(), name="api-menu"),
  path('api-menu/<int:pk>', views.SingleMenuItemView.as_view(), name="api-single-menu"),
  path('api-token-auth', obtain_auth_token, name="api-token-auth"),
]
