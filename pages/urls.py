from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]