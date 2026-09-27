from django.urls import path
from OrientationApp import views

urlpatterns = [
    path('', views.View, name='View')
]