from django.urls import path

from . import views

app_name = 'parking'
urlpatterns = [
    path("", views.index, name="index"),
    path('book/', views.book, name="book"),
    path('<str:parking_address>/confirmation/', views.confirmation, name='confirmation'),
    path('result/', views.result, name='result'),
    path('checkout_page/', views.checkout_page, name='checkout_page'),
    path('checkout/', views.checkout, name='checkout')
    ]
