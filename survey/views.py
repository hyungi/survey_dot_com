from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import SurveyForm
from .models import Survey, SurveyProduce, SurveyRespond, SurveyInterest
from member.models import Member
# survey/views.py


# Survey CRUD
def new_survey(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = SurveyForm(request.POST)
            if form.is_valid():
                survey = form.save()
                member = Member.objects.get(pk=request.user.id)
                survey_produce = SurveyProduce.objects.create(member=member, survey=survey)
                print(survey_produce)
                return redirect('my_survey', pk=survey.pk)

        else:
            form = SurveyForm()

        return render(request, 'survey/survey_edit.html', {'form': form})


def edit_survey(request, pk):
    if request.user.is_authenticated():
        survey = get_object_or_404(Survey, pk=pk)
        if request.method == "POST":
            form = SurveyForm(request.POST, instance=survey)
            if form.is_valid():
                survey = form.save()

                return redirect('my_survey', pk=survey.pk)

        else:
            form = SurveyForm(instance=survey)

        return render(request, 'survey/survey_edit.html', {'form': form})


def my_survey_list(request):
    if request.user.is_authenticated():
        '''
        Member -> SurveyProduce -> Survey
        '''
        pk = request.user.id
        member = Member.objects.get(pk=pk)
        survey_produces = SurveyProduce.objects.filter(member=member).order_by('-produce_date')

        surveys = []

        for survey_produce in survey_produces:
            print("in my_survey_list_view: " + str(survey_produce))
            print(survey_produce.survey.pk)
            surveys += Survey.objects.filter(pk=survey_produce.survey.pk).values()

        print(surveys)
        return render(request, 'survey/my_survey_list.html', {'surveys': surveys})


def my_survey(request, pk):
    if request.user.is_authenticated():
        survey = Survey.objects.get(pk=pk)
        return render(request, 'survey/my_survey.html', {'survey': survey})


def all_survey_list(request):
    if request.user.is_authenticated():
        pk = request.user.id
        member = Member.objects.get(pk=pk)
        surveys = Survey.objects.all()
        survey_interests = SurveyInterest.objects.select_related('survey').all().annotate(count=Count('survey'))
        return render(request, 'survey/all_survey_list.html', {
            'member': member,
            'surveys': surveys,
            'survey_interests': survey_interests,
        })

    else:
        return render(request, 'home.html')


def del_survey(request, pk):
    # survey pk 가 넘어온다
    if request.user.is_authenticated():
        survey = Survey.objects.filter(pk=pk).values()

        print("이 친구를 지우는 거..! ")
        print(survey)
        return render(request, 'profile.html')


def detail_survey(request, pk):
    # survey의 기본 정보을 보여준다.
    if request.user.is_authenticated():
        survey = Survey.objects.get(pk=pk)
        # 이 서베이의 주인이 아님을 확인
        if SurveyProduce.objects.filter(pk=pk, member=request.user.id).count() == 0:
            interest_count = SurveyInterest.objects.filter(survey=survey).count()
            print(interest_count)
            already_interested = SurveyInterest.objects.filter(survey=survey, member=request.user.id).count()
            print(already_interested)
            survey.view_count += 1
            survey.save()
            return render(request, 'survey/detail_survey.html', {
                'survey': survey,
                'interest_count': interest_count,
                'already_interested': already_interested,
            })

        else:
            return render(request, 'survey/my_survey.html', {'survey': survey})


def respond_survey(request, pk):
    if request.user.is_authenticated():
        member = Member.objects.get(pk=request.user.id)
        survey = Survey.objects.get(pk=pk)
        survey_respond_count = SurveyRespond.objects.filter(member=member, survey=survey).count()
        if survey_respond_count == 0:
            # 응답을 중복하지 않도록!
            survey_respond = SurveyRespond.objects.create(member=member, survey=survey)
            print(survey_respond)
            return render(request, 'survey/detail_survey.html', {
                'survey': survey,
                'survey_respond_count': survey_respond_count
            })
        else:
            print("이미 응답한 적이 있습니다!")
            return render(request, 'survey/detail_survey.html', {
                'survey': survey,
                'survey_respond_count': survey_respond_count
            })


def interest_survey(request, pk):
    if request.user.is_authenticated():
        member = Member.objects.get(pk=request.user.id)
        survey = Survey.objects.get(pk=pk)
        if SurveyProduce.objects.filter(member=member, survey=survey).count() == 0:
            survey_interest = SurveyInterest.objects.filter(member=member, survey=survey)
            if survey_interest.count() == 0:
                # 관심 표현한적 없을때만!
                SurveyInterest.objects.create(member=member, survey=survey)
                print("관심표시!")
                return render(request, 'survey/detail_survey.html', {'survey': survey})
            else:
                survey_interest.delete()
                print("관심표시 취소!")
                return render(request, 'survey/detail_survey.html', {'survey': survey})

        else:
            print("자기가 만든 서베이는 관심 표시 금지!")
            return render(request, 'survey/detail_survey.html', {'survey': survey})

# def apply_group(request, pk):
#     if request.user.is_authenticated():
#         member_id = request.user.id
#         group = Group.objects.get(pk=pk)
#         print(Belong.objects.filter(member=member_id, group=group).exists())
#
#         if Belong.objects.filter(member=member_id, group=group).exists() is True:
#             print("이미 가입한 그룹이야~")
#             return redirect('my_group_list', pk=member_id)
#         member = Member.objects.get(pk=member_id)
#         new_belong = Belong.objects.create(member=member, group=group)
#         # new_belong.save()
#         return redirect('my_group_list', pk=member_id)
#
#
# def new_group(request):
#     if request.user.is_authenticated():
#         if request.method == "POST":
#             form = GroupForm(request.POST)
#             if form.is_valid():
#                 group = form.save(commit=False)
#                 member = Member.objects.get(pk=request.user.id)
#                 group.save()
#                 Belong.objects.create(member=member, group=group)
#
#                 return redirect('my_group_detail', pk=group.pk)
#
#         else:
#             form = GroupForm()
#
#         return render(request, 'group/group_edit.html', {'form': form})
#
#
# def group_edit(request, pk):
#     if request.user.is_authenticated():
#         group = get_object_or_404(Group, pk=pk)
#         if request.method == "POST":
#             form = GroupForm(request.POST, instance=group)
#             if form.is_valid():
#                 group = form.save(commit=False)
#                 group.save()
#                 return redirect('my_group_detail', pk=group.pk)
#
#         else:
#             form = GroupForm(instance=group)
#
#         return render(request, 'group/group_edit.html', {'form': form})
#
#
# def all_group_list(request):
#     if request.user.is_authenticated():
#         groups = Group.objects.all().values()
#         return render(request, 'group/all_group_list.html', {'groups': groups})
#
#
# def my_group_list(request, pk):
#     if request.user.is_authenticated():
#         '''
#         member -> belong -> group
#         '''
#         member = Member.objects.filter(pk=pk)
#         belongs = Belong.objects.filter(member_id=member).values()
#
#         # surveys = Survey.objects.all()
#         print(belongs)
#         return render(request, 'group/my_group_list.html', {'belongs': belongs})
#
#
# def my_group_detail(request, pk):
#     if request.user.is_authenticated():
#         group_infos = Group.objects.filter(pk=pk).values()
#
#         print(group_infos)
#         return render(request, 'group/group_detail.html', {'group_infos': group_infos})
