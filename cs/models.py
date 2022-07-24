from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy


# python manage.py runserver
# python manage.py makemigrations
# python manage.py migrate

class Tournament(models.Model):

    def get_upload_path(self, filename):
        return f"photos/tournaments/{self.slug}/{filename}"

    def get_rules_path(self, filename):
        return f"files/rules/{self.slug}/{filename}"

    def get_absolute_url(self):
        return reverse('tournament_info', kwargs={'slug': self.slug})


    title = models.CharField(max_length=150, verbose_name="Заголовок")
    game = models.ForeignKey("Game", on_delete=models.SET_DEFAULT, default="Игра не указана", verbose_name="Игра")
    prize_fund = models.TextField(blank=True, verbose_name="Призовой фонд")
    prize_1 = models.CharField(max_length=255, blank=True, verbose_name="Приз для 1-го места")
    prize_2 = models.CharField(max_length=255, blank=True, verbose_name="Приз для 2-го места")
    prize_3 = models.CharField(max_length=255, blank=True, verbose_name="Приз для 3-го места")
    another_prizes = models.TextField(blank=True, verbose_name="Призы для дургих мест")
    descr = models.TextField(verbose_name="Описание")
    time_start = models.DateTimeField(verbose_name="Время начала")
    team_members = models.PositiveSmallIntegerField(verbose_name="Участников в команде")
    creator = models.TextField(max_length=100, verbose_name="Огранизатор")
    contact = models.URLField(blank=True, verbose_name="Ссылка для связи")
    contact_email = models.EmailField(verbose_name="Почта для связи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_changed = models.DateTimeField(auto_now=True, verbose_name="Время последнего редактирования")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    slug = models.SlugField(unique=True, verbose_name="URL")
    rules = models.FileField(upload_to=get_rules_path, blank=True, verbose_name="Правила")
    photo = models.ImageField(upload_to=get_upload_path, verbose_name="Фото")
    broadcast_url = models.URLField(blank=True, verbose_name="Ссылка на трансляцию")
    teams = models.ManyToManyField('Team', related_name='tournaments')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"
        ordering = ['-time_start', 'game', '-prize_fund', 'creator']


class User(AbstractUser):
    def get_upload_path(self, filename):
        return f"photos/users/{self.slug}/{filename}"

    SEX_CHOICES = (
        ('М', 'Мужской '),
        ('Ж', 'Женский'),
    )

    patronymic = models.CharField(max_length=30, blank=True, verbose_name="Отчество")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Пол")
    bio = models.TextField(max_length=700, blank=True, verbose_name="Доп. информация")
    phone = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name="Телефон")
    stud_num = models.IntegerField(verbose_name="Номер студ. билета", blank=True, null=True)
    is_verified = models.BooleanField(default=False, verbose_name="Подтверждён")
    slug = models.SlugField(unique=True, verbose_name="URL")
    photo = models.ImageField(upload_to=get_upload_path, default="photos/users/default.svg", verbose_name="Фото")

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse_lazy('user_info', kwargs={"slug": self.slug,})

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Game(models.Model):
    def get_upload_path(self, filename):
        return f"photos/games/{self.slug}/{filename}"

    short_name = models.CharField(max_length=10, unique=True, verbose_name="Короткое название")
    long_name = models.CharField(max_length=150, unique=True, verbose_name="Полное название")
    descr_url = models.URLField(blank=True, verbose_name="Описание")
    slug = models.SlugField(unique=True, verbose_name="URL")
    photo = models.ImageField(upload_to=get_upload_path, verbose_name="Фото")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['short_name', 'long_name']


    def __str__(self):
        return self.short_name


class Team(models.Model):
    def get_upload_path(self, filename):
        return f"photos/teams/{self.slug}/{filename}"

    users = models.ManyToManyField(User, related_name='teams', verbose_name="Игроки")
    short_name = models.CharField(max_length=10, unique=True, verbose_name="Короткое название")
    long_name = models.CharField(max_length=150, unique=True, verbose_name="Полное название")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    slug = models.SlugField(unique=True, verbose_name="URL")
    photo = models.ImageField(upload_to=get_upload_path, verbose_name="Фото",
                              default="photos/teams/default_team_logo.png")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    bio = models.TextField(max_length="700", blank=True, verbose_name="Доп. информация")
    tours_1_place = models.ManyToManyField(Tournament, related_name="teams_1_place", blank=True)
    tours_2_place = models.ManyToManyField(Tournament, related_name="teams_2_place", blank=True)
    tours_3_place = models.ManyToManyField(Tournament, related_name="teams_3_place", blank=True)

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse_lazy('team_info', kwargs={"slug": self.slug,})

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"
        ordering = ['-time_create', 'short_name', 'long_name', 'creator']


class Tournament_Team_User(models.Model):

    tournament = models.ForeignKey(Tournament, verbose_name="Турнир", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, verbose_name="Команда", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Игрок", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tournament} - {self.team} - {self.user}"

    class Meta:
        verbose_name = "Туринр - команда - игрок"
        verbose_name_plural = "Туринры - команды - игроки"
        ordering = ['tournament', 'team', 'user']


# python manage.py runserver
# python manage.py makemigrations
# python manage.py migrate
