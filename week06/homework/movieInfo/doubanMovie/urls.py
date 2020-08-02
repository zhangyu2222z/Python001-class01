from django.urls import path
from . import views

urlpatterns = [
    path('', views.favourableComment),
    path('loadInfo', views.movieReview),
    path('loadThreeStars', views.favourableComment),
]
