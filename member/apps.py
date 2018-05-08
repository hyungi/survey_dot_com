from django.apps import AppConfig


class MemberConfig(AppConfig):
    name = 'member'
    verbose_name = 'member Config for User'

    def ready(self):
        import member.signals

