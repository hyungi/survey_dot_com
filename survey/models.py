from django.db import models
from django.utils import timezone
from member.models import Member, Category
# survey/models.py


class SurveyImage(models.Model):
    image_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Survey(models.Model):
    title = models.CharField(max_length=100, default="")
    summary = models.TextField()
    content = models.TextField()
    form_link = models.URLField()
    view_count = models.PositiveIntegerField(default=0)
    edit_count = models.PositiveIntegerField(default=0)
    recent_view_date = models.DateTimeField(default=timezone.now)
    recent_edit_date = models.DateTimeField(default=timezone.now)
    feedback_count = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now()+timezone.timedelta(days=10))
    additional_respond_flag = models.BooleanField(default=False)
    survey_image = models.ImageField(null=True)
    survey_image_id = models.ForeignKey(SurveyImage, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "제목: [" + str(self.title) + "], 요약: [" + str(self.summary) + "]"


class SurveyMemberForeignKey(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class SurveyProduce(SurveyMemberForeignKey):
    produce_date = models.DateTimeField(default=timezone.now)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.member) + "가 " + str(self.produce_date) + " 에 만든 " + str(self.survey)


class SurveyRespond(SurveyMemberForeignKey):
    respond_date = models.DateField(default=timezone.now)
    respond_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return str(self.survey) + "에 대한, " + str(self.member) + "의 응답"


class SurveyInterest(SurveyMemberForeignKey):
    interest_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.survey) + "에 대한, " + str(self.member) + "의 관심"


class SurveyView(SurveyMemberForeignKey):
    view_date = models.DateTimeField(default=timezone.now)


class SurveyComment(SurveyMemberForeignKey):
    comment_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    recent_edit_time = models.DateTimeField(default=timezone.now)


class SurveyFeedback(SurveyMemberForeignKey):
    feedback_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, default="")
    summary = models.TextField()
    content = models.TextField()
    rating = models.IntegerField(default=0)
    recent_edit_date = models.DateTimeField(default=timezone.now)


class SurveySubscribe(SurveyMemberForeignKey):
    subscribe_date = models.DateTimeField(default=timezone.now)
    subscribe_period = models.DateTimeField(default=timezone.now)
    view_count = models.IntegerField(default=0)
    recent_view_datetime = models.DateTimeField(default=timezone.now)


class SurveyAuthority(models.Model):
    authority_name = models.CharField(max_length=100, default="")
    description = models.TextField()


class SurveyAuthoritySetting(SurveyMemberForeignKey):
    authority_setting_date = models.DateTimeField(default=timezone.now)
    survey_authority = models.ForeignKey(SurveyAuthority, on_delete=models.CASCADE)


class TargetAge(models.Model):
    age_range = models.CharField(max_length=100, default="")
    description = models.TextField()


class TargetLocation(models.Model):
    location_name = models.CharField(max_length=100, default="")
    description = models.TextField()


class TargetStatus(models.Model):
    status_name = models.CharField(max_length=100, default="")
    description = models.TextField()


class TargetSetting(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    target_age = models.ForeignKey(TargetAge, on_delete=models.CASCADE)
    target_location = models.ForeignKey(TargetLocation, on_delete=models.CASCADE)
    target_status = models.ForeignKey(TargetStatus, on_delete=models.CASCADE)


# 이 아래로는 legacy table


# class Belong(models.Model):
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)


# 기본 키(Primary, ID) 는 자동으로 추가됩니다.
# class Group(models.Model):
#     # group_id = models.CharField(max_length=100, primary_key=True)
#     group_name = models.CharField(max_length=100, default="")
#     group_project = models.CharField(max_length=100, default="")
#     group_goal = models.CharField(max_length=100, default="")
#     start_date = models.DateTimeField(default="")
#     end_date = models.DateTimeField(default="")
