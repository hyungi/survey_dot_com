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
    birth = models.DateField(default=timezone.datetime(1992, 1, 1))
    group = models.CharField(max_length=100, default="")
    company = models.CharField(max_length=100, null=True)
    major = models.CharField(max_length=100, default="")
    email = models.EmailField(default="")
    google_uid = models.CharField(max_length=100, default="")
    facebook_uid = models.CharField(max_length=100, default="")
    naver_uid = models.CharField(max_length=100, default="")
    member_status = models.ForeignKey(MemberStatus, on_delete=models.CASCADE, null=True)

    def incomplete_member(self):
        if self.name == u"":
            return False
        elif self.major == u"":
            return False
        elif self.birth is None:
            return False
        elif self.email == u"":
            return False
        return True

    def __str__(self):
        return "Member: " + self.name


class Query(models.Model):
    query_name = models.DateTimeField(default=timezone.now)


class Search(models.Model):
    search_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE, null=True)
