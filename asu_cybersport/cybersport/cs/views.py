from django.http import HttpResponse
from django.shortcuts import render
from .models import *

menu = ['О сайте', "Турниры", "Контакты", "Подать заявку", "Вход", "Регистрация"]

def index(request):
    return render(request, 'cs/index.html', {'menu': menu, 'title': 'ASU CyberSport', 'content': 'Главная страница сайта ASU CyberSport'})

def about(request):
    return render(request, 'cs/about.html', {'menu': menu, 'title': 'Контакты', 'content': 'Контакты ASU CyberSport'})

#def contacts(request):
#    return render(request, 'contacts.html')
#
#def tournaments(request):
#    return render(request, 'tournaments.html')
