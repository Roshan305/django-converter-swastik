from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('translate/', views.translate_text, name='translate'),
    path('convert-currency/', views.convert_currency, name='convert_currency'),
]