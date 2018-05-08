from allauth.account.signals import user_logged_in, user_signed_up
from django.dispatch import receiver
from django.utils import timezone

from member.models import Member


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    print("def user_logged_in_")
    if user.is_active is False:
        print("예외 처리 해보자")
    if kwargs.get('sociallogin').account.provider == 'facebook':
        print(kwargs.get('sociallogin').account.extra_data)
    elif kwargs.get('sociallogin').account.provider == 'naver':
        print(kwargs.get('sociallogin').account.extra_data)
    else:
        print(kwargs.get('sociallogin').account.extra_data)


@receiver(user_signed_up)
def user_signed_up_(request, user, sociallogin=None, **kwargs):
    print("in def user_signed_up_")
    print(user.id)
    print(request)
    name = "default_name"
    nick_name = "default_nick_name"

    pk = user.id

    if sociallogin.account.provider == 'facebook':
        print('facebook' + str(sociallogin.account.extra_data))
        fid = sociallogin.account.extra_data['id']
        email = sociallogin.account.extra_data['email']
        name = sociallogin.account.extra_data['name']
        member = Member(
            pk=pk,
            name=name,
            nick_name=name,
            registered_date=timezone.now(),
            company="",
            major="",
            email=email,
            google_uid=0,
            facebook_uid=fid,
            naver_uid=0,
        )
        member.save()
        print(member)

    elif sociallogin.account.provider == 'naver':
        print(sociallogin.account.extra_data)
        nid = sociallogin.account.extra_data['id']
        # name = sociallogin.account.extra_data['name']
        # nick_name = sociallogin.account.extra_data['nick_name']
        email = sociallogin.account.extra_data['email']
        member = Member(
            pk=pk,
            name=name,
            nick_name=nick_name,
            registered_date=timezone.now(),
            company="",
            major="",
            email=email,
            google_uid=0,
            facebook_uid=0,
            naver_uid=nid,
        )
        member.save()
        print(sociallogin.account.provider)

    elif sociallogin.account.provider == 'google':
        print('google' + str(sociallogin.account.extra_data))
        gid = sociallogin.account.extra_data['id']
        print(dir(sociallogin.account))
        email = sociallogin.account.extra_data['email']
        name = sociallogin.account.extra_data['name']
        member = Member(
            pk=pk,
            name=name,
            nick_name=name,
            registered_date=timezone.now(),
            company="",
            major="",
            email=email,
            google_uid=gid,
            facebook_uid=0,
            naver_uid=0,
        )
        member.save()
        print(member)
