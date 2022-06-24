from django.urls import path

from .views import *


urlpatterns = [
    path('', index),
    path('about/', about, name='about'),
    #path('contacts/', contacts, name='contacts'),
    #path('tournaments/', tournaments, name='tournaments'),
]