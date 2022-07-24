from django.contrib.auth import logout
from django.contrib.auth.forms import *
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseNotFound, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *


from .forms import SignUpForm, LoginForm, CreateTeamForm, EditTeamForm
from .models import *
from .utils import *


def index(request):
    return render(request, 'cs/index.html',
                  {'menu': menu, 'site_name': site_name, 'title': "Главная страница", 'login_menu': login_menu})

def about(request):
    return render(request, 'cs/about.html',
                  {'menu': menu, 'site_name': site_name, 'title': "О проекте", 'login_menu': login_menu})

def contacts(request):
    return render(request, 'cs/contacts.html',
                  {'menu': menu, 'site_name': site_name, 'title': "Контакты", 'login_menu': login_menu})

def logout_user(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))  # редирект на ту же страницу


def edit_team(request, slug):

    if not request.user.is_authenticated:
        return redirect('login', permanent=True)
    team = get_object_or_404(Team, slug=slug)
    if team.creator != request.user:
        return redirect('team_info', slug=slug)

    if request.method == 'POST':
        print("method == 'POST'")
        form = EditTeamForm(request.POST, request.FILES, team_id=team.pk)
        if form.is_valid():
            print('form is valid')
            team.save()
            return redirect('team_info', slug=slug)
    else:
        form = EditTeamForm(instance=team, team_id=team.pk)

    members = team.users.all().exclude(pk=request.user.pk)
    context = {'menu': menu, 'site_name': site_name, 'title': f"{team} | Редактирование", 'login_menu': login_menu,
               'form': form, 'creator': team.creator, 'members': members}
    return render(request, 'cs/edit_team.html', context=context)

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h>")

class TournamentsList(DataMixin, ListView):
    model = Tournament
    template_name = 'cs/tournaments.html'
    context_object_name = 'tours'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Турниры')
        return context | mixin_context

    def get_queryset(self):
        return Tournament.objects.filter(is_published=True)


class TournamentInfo(DataMixin, DetailView):
    model = Tournament
    template_name = 'cs/tournament_info.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'tour'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context()
        return context | mixin_context


class TeamsList(DataMixin, ListView):
    model = Team
    template_name = 'cs/teams.html'
    context_object_name = 'teams'
    ordering = ['tours_1_place', 'tours_2_place', 'tours_3_place', 'tournaments']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Команды')
        return context | mixin_context


class MyTeamsList(TeamsList):
    template_name = 'cs/my_teams.html'

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login', permanent=True)
        else:
            return super().get(self, request)


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) | self.get_user_context(title='Мои команды')
        teams = User.objects.get(username=self.request.user).teams.all().\
            order_by('tours_1_place', 'tours_2_place', 'tours_3_place', 'tournaments')
        teams_member = teams.filter(~Q(creator=self.request.user))  # команды где пользователь участник
        teams_creator = teams.filter(creator=self.request.user)  # команды где пользователь капитан
        context['teams_member'] = teams_member
        context['teams_creator'] = teams_creator
        return context


class TeamInfo(DataMixin, DetailView):
    model = Team
    template_name = 'cs/team_info.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'team'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context()
        return context | mixin_context


class CreateTeam(DataMixin, CreateView):
    form_class = CreateTeamForm
    template_name = 'cs/create_team.html'

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login', permanent=True)
        else:
            return super().get(self, request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Создание команд')
        return context | mixin_context

    def get_success_url(self):
        return reverse_lazy('my_teams')

    def form_valid(self, form):
        form_instance = form.save(commit=False)  # сохраняем модель из формы в БД с данными (без участников и создателя)
        form_instance.creator = self.request.user  # добавляем создателя и сохраняем, чтобы
        form_instance.save()  # появилась запись с ID
        form_instance.users.add(self.request.user)  # и с помощью этого ID, добавляем в M2M поле users учатника -
        form_instance.save()  # создателя. И сохраняем форму в БД
        return redirect('my_teams')


class SignUp(DataMixin, CreateView):
    form_class = SignUpForm
    template_name = 'cs/signup.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Регистрация')
        return context | mixin_context


class Login(DataMixin, LoginView):
    form_class = LoginForm
    template_name = 'cs/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin_context = self.get_user_context(title='Вход')
        return context | mixin_context

    def get_success_url(self):
        return reverse_lazy('main')


class UserInfo(DataMixin, DetailView):
    model = User
    template_name = 'cs/user_info.html'
    context_object_name = 'user_info'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs) | self.get_user_context(title='Мои команды')
        return context



