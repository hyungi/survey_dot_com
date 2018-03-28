import logging
from allauth.account.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def user_logged_in_(request, user):
    logger = logging.getLogger(__name__)
    logger.debug("user logging in: %s at %s" % (user, request.META['REMOTE_ADDR']))
    print(user)
    print(request)
