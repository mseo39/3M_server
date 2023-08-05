from django.contrib import admin
from django.urls import path,include
import user.views

urlpatterns = [
    path('signup', user.views.signup, name='signup'),
    path('signin', user.views.signin, name='signin'),
    path('useridcheck', user.views.useridcheck, name='useridcheck'),
    path('delete', user.views.delete, name='delete')
]