from django.contrib import admin
from django.urls import path,include
import reportcheck.views

urlpatterns = [
    path('myreport', reportcheck.views.myreport, name='myreport'),
    path('mycar', reportcheck.views.mycar, name='mycar')
]
