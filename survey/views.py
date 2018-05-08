from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import SurveyForm
from .models import Survey, SurveyProduce, SurveyRespond, SurveyInterest
from member.models import Member


# survey/views.py


# Survey Search
@csrf_protect
@login_required
def search_survey(request):
    if request.method == 'POST':
        query = request.POST['query']
        pk = request.user.id
        member = Member.objects.get(pk=pk)
        surveys = Survey.objects.filter(title__contains=query)
        survey_interests = SurveyInterest.objects.select_related('survey').all().annotate(count=Count('survey'))
        return render(request, 'survey/search_result.html', {
            'member': member,
            'surveys': surveys,
            'survey_interests': survey_interests,
        })


# Survey CRUD
@login_required
def new_survey(request):
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


@login_required
def edit_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        form = SurveyForm(request.POST, request.FILES, instance=survey)
        if form.is_valid():
            survey = form.save()

            return redirect('my_survey', pk=survey.pk)

    else:
        form = SurveyForm(instance=survey)

    return render(request, 'survey/survey_edit.html', {'form': form})


@login_required
def my_survey_list(request):
    """
    Member -> SurveyProduce -> Survey
    """
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


@login_required
def my_survey(request, pk):
    if request.user.is_authenticated:
        survey = Survey.objects.get(pk=pk)
        return render(request, 'survey/my_survey.html', {'survey': survey})


@login_required
def all_survey_list(request):
    member = Member.objects.get(pk=request.user.id)
    surveys = Survey.objects.all()
    survey_interests = SurveyInterest.objects.values('survey').annotate(count=Count('survey')).order_by('-count')
    my_interests = SurveyInterest.objects.filter(member=member)

    print(survey_interests.count)
    return render(request, 'survey/all_survey_list.html', {
        'member': member,
        'surveys': surveys,
        'survey_interests': survey_interests,
        'my_interests': my_interests,
    })


@login_required
def del_survey(request, pk):
    # survey pk 가 넘어온다
    survey = Survey.objects.get(pk=pk)
    survey.delete()

    return redirect('my_survey_list')


@login_required
def detail_survey(request, pk):
    # survey의 기본 정보을 보여준다.
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


@login_required
def respond_survey(request, pk):
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


@login_required
def interest_survey(request, pk):
    member = Member.objects.get(pk=request.user.id)
    survey = Survey.objects.get(pk=pk)
    if SurveyProduce.objects.filter(member=member, survey=survey).count() == 0:
        survey_interest = SurveyInterest.objects.filter(member=member, survey=survey)
        if survey_interest.count() == 0:
            # 관심 표현한적 없을때만!
            SurveyInterest.objects.create(member=member, survey=survey)
            print("관심표시!")
            # return redirect('detail_survey', survey='survey')
            return render(request, 'survey/detail_survey.html', {'survey': survey})
        else:
            survey_interest.delete()
            print("관심표시 취소!")
            return render(request, 'survey/detail_survey.html', {'survey': survey})

    else:
        print("자기가 만든 서베이는 관심 표시 금지!")
        return render(request, 'survey/detail_survey.html', {'survey': survey})
