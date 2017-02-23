from django.conf.urls import url, include
from django.contrib import admin

from . import views

app_name = 'member'
urlpatterns = [
    url('^login/$', views.login_fbv, name='login')
]
