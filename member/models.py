from allauth.account.signals import user_logged_in, user_signed_up
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

# member/models.py


# Survey 와 Draft 의 순환참조 문제로 아예 무관한 Member app 으로 옮겨옴
class Category(models.Model):
    category_name = models.CharField(max_length=100, default="")
    description = models.TextField()


class MemberStatus(models.Model):
    status_name = models.CharField(max_length=100, default="")
    description = models.TextField()


class Member(models.Model):
    # member_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=50, default="")
    nick_name = models.CharField(max_length=50, default="")
    registered_date = models.DateTimeField(default=timezone.now)
    birth = models.DateTimeField(default=timezone.now)
    group = models.CharField(max_length=100, default="")
    company = models.CharField(max_length=100, default="")
    major = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    google_uid = models.CharField(max_length=100, default="")
    facebook_uid = models.CharField(max_length=100, default="")
    naver_uid = models.CharField(max_length=100, default="")
    member_status = models.ForeignKey(MemberStatus, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Member: " + self.name


class Query(models.Model):
    query_name = models.DateTimeField(default=timezone.now)


class Search(models.Model):
    search_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE, null=True)


@receiver(user_logged_in)
def user_logged_in_(request, user, **kwargs):
    print("def user_logged_in_")
    print(user.id)
    print(user)
    print(request)
    if kwargs.get('sociallogin').account.provider == 'facebook':
        print(kwargs.get('sociallogin').account.extra_data['id'])
        print(kwargs.get('sociallogin').account.extra_data['email'])
        print(kwargs.get('sociallogin').account.extra_data['name'])
    else:
        print(kwargs.get('sociallogin').account.extra_data['id'])
        age = kwargs.get('sociallogin').account.extra_data['age']
        print(age)
        print(kwargs.get('sociallogin').account.extra_data['email'])
        print((int(age.split("-", 1)[0]) + int(age.split("-", 1)[1]))/2)


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
            company="test_company",
            major="test_major",
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
            company="test_company",
            major="test_major",
            email=email,
            google_uid=0,
            facebook_uid=0,
            naver_uid=nid,
        )
        member.save()

        print(sociallogin.account.provider)
