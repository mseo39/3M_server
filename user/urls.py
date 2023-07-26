from django.contrib import admin
from django.urls import path,include
import user.views

urlpatterns = [
    path('signup', user.views.signup, name='signup')
]