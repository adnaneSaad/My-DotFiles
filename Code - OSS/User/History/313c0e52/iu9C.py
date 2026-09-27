from django.urls import path
from . import views

urlpatterns = [
    path('', views.SR72, name='SR72'),
]
