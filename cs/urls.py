from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='main'),
    path('about/', about, name='about'),
    path('contacts/', contacts, name='contacts'),
    path('tournaments/', TournamentsList.as_view(), name='tournaments'),
    path('tournaments/<slug:slug>/', TournamentInfo.as_view(), name='tournament_info'),
    path('login/', Login.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('logout/', logout_user, name='logout'),
    path('create-team/', CreateTeam.as_view(), name='create_team'),
    path('teams/', TeamsList.as_view(), name='teams'),
    path('teams/my-teams/', MyTeamsList.as_view(), name='my_teams'),
    path('teams/<slug:slug>/', TeamInfo.as_view(), name='team_info'),
    path('teams/<slug:slug>/edit/', edit_team, name='edit_team'),
    path('users/<slug:slug>/', UserInfo.as_view(), name='user_info'),
]