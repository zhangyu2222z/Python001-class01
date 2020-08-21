from django.urls import path
from . import views

urlpatterns = [
    path('', views.logon),
    path('enter', views.enter),
]