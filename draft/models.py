from django.db import models
from django.utils import timezone
from member.models import Member, Category
from survey.models import Survey
# draft/models.py


class Draft(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    view_count = models.PositiveIntegerField(default=0)
    edit_count = models.PositiveIntegerField(default=0)
    recent_view_date = models.DateTimeField(default=timezone.now)
    recent_edit_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, default=None, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "title: " + self.title + " content: " + self.content


class MemberDraftForeignKey(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class DraftProduce(MemberDraftForeignKey):
    produce_date = models.DateTimeField(default=timezone.now)


class DraftView(MemberDraftForeignKey):
    view_date = models.DateTimeField(default=timezone.now)


class DraftInterest(MemberDraftForeignKey):
    interest_date = models.DateTimeField(default=timezone.now)


class DraftComment(MemberDraftForeignKey):
    comment_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    recent_edit_time = models.DateTimeField(default=timezone.now)


class Vote(models.Model):
    vote_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    draft = models.ForeignKey(Draft, on_delete=models.CASCADE)


class Option(models.Model):
    content = models.CharField(max_length=100)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)


class VoteRespond(models.Model):
    respond_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
