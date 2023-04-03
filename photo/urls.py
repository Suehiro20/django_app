from django.urls import path
from . import views

app_name = "photo"

urlpatterns = [
    path('', views.PhotoIndexView.as_view(), name='index'),
]