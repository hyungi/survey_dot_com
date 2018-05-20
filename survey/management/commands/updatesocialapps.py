from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from allauth.socialaccount.models import SocialApp
from django.core.exceptions import ImproperlyConfigured, MultipleObjectsReturned, ObjectDoesNotExist
from django.contrib.sites.models import Site
import re
import os
import json

class Command(BaseCommand):
    help = 'Loads app settings to allauth from social.json'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        secret_file = os.path.join(settings.BASE_DIR, 'envs.json')
        with open(secret_file) as f:
            secrets = json.loads(f.read())

        sites = settings.ALLOWED_HOSTS
        if settings.DEBUG:
            sites.append('*')
        
        providers = [ 'facebook', 'naver', 'google' ]
        for provider in providers:
            key_key = provider.upper() + '_KEY'
            secret_key = provider.upper() + '_SECRET'
            name = provider + '_login'

            try:
                key = secrets[key_key]
                secret = secrets[secret_key]
            except KeyError:
                print('{} or {} does not exist in env.json'.format(key_key, secret_key))
                print('skipping {}...'.format(provider))
            else:
                try:
                    app = SocialApp.objects.all().get(provider=provider)
                except ObjectDoesNotExist:
                    app = SocialApp(provider=provider,
                              name=name,
                              client_id=key,
                              secret=secret)
                    print('added FaceBook SocialApp w/ key {}'.format(key))
                except MultipleObjectsReturned:
                    app = None
                    print('fatal: multiple {} SocialApp objects'.format(provider))
                    print('skipping {}...'.format(provider))
                else:
                    app.client_id = key 
                    app.secret = secret 
                    print('updated {} SocialApp w/ key {}'.format(provider, key))
                finally:
                    if app:
                        app.save()
                        app.sites.clear()
                        app.sites.add(*Site.objects.all()) # hmm
