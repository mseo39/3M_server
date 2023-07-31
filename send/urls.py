from django.contrib import admin
from django.urls import path,include
import send.views

urlpatterns = [
    path('Data', send.views.Data, name='Data'),
]
