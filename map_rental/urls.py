from django.urls import path
from . import views

urlpatterns = [
    path('', views.rental_map, name='rental_map'),
]