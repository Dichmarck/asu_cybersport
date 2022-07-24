from django.contrib import admin

from cs.models import *


class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'photo', 'title', 'game', 'prize_fund', 'time_start', 'creator', 'is_published')
    filter_horizontal = ['teams']


class UserAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("username",)}
    list_display = ('id', 'photo', 'username', 'first_name', 'last_name', 'is_verified', 'date_joined', 'last_login')


class GameAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}
    list_display = ('id', 'photo', 'short_name', 'long_name', 'slug')


class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}
    list_display = ('id', 'photo', 'short_name', 'long_name', 'creator', 'slug')
    filter_horizontal = ['users', 'tours_1_place', 'tours_2_place', 'tours_3_place']


class Tournament_Team_UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tournament', 'team', 'user')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament_Team_User, Tournament_Team_UserAdmin)
