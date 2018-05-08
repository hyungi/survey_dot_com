from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from survey.models import SurveyInterest, SurveyRespond
from .forms import MemberForm
from .models import Member
from django.contrib.auth.models import User
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
# member/views.py

# class SocialAccountAdapter(DefaultSocialAccountAdapter):


def member_info(request):
    if request.user.is_authenticated:
        pk = request.user.id
        print(pk)
        member = Member.objects.get(pk=pk)

        if member.incomplete_member() is False:
            return redirect('member_edit')

        popular_surveys = SurveyInterest.objects.select_related('survey').all().annotate(count=Count('survey')).order_by('-count')[:10]
        print(popular_surveys)
        survey_interests = SurveyInterest.objects.filter(member=member)
        survey_responds = SurveyRespond.objects.filter(member=member)
        print("member_info: " + str(member))
        return render(request, 'member/member_info.html', {
            'member': member,
            'survey_interests': survey_interests,
            'survey_responds': survey_responds,
            'popular_surveys': popular_surveys,
        })


def member_edit(request):
    if request.user.is_authenticated:
        pk = request.user.id
        print(pk)
        member = get_object_or_404(Member, pk=pk)
        if request.method == "POST":
            form = MemberForm(request.POST, instance=member)
            if form.is_valid():
                member = form.save(commit=False)
                member.save()
                return redirect('member_info')

        else:
            form = MemberForm(instance=member)

        return render(request, 'member/member_edit.html', {'form': form})


def sign_out(request, pk):
    if request.user.is_authenticated:
        # member = Member.objects.get(pk=pk)
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        print("이 친구를 지우는 거..! " + str(user.is_active))
        # member.delete()
        return render(request, 'index.html')
