site_name = "ASU CyberSport"
menu = [{'title': 'О проекте', 'url_name': 'about'},
        {'title': 'Турниры', 'url_name': 'tournaments'},
        {'title': "Мои команды", 'url_name': 'my_teams'},
        {'title': "Список команд", 'url_name': 'teams'},
        {'title': "Контакты", 'url_name': 'contacts'},
        ]
login_menu = [{'title': 'Вход', 'url_name': 'login'}, {'title': 'Регистрация', 'url_name': 'signup'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['site_name'] = site_name
        context['login_menu'] = login_menu

        return context
