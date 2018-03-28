from django.shortcuts import render, get_object_or_404, redirect

from survey.models import SurveyInterest, SurveyRespond
from .forms import MemberForm
from .models import Member
# member/views.py


def member_info(request):
    if request.user.is_authenticated:
        pk = request.user.id
        print(pk)
        member = Member.objects.get(pk=pk)

        survey_interests = SurveyInterest.objects.filter(member=member)
        survey_responds = SurveyRespond.objects.filter(member=member)
        print("member_info: " + str(member))
        return render(request, 'member/member_info.html', {
            'member': member,
            'survey_interests': survey_interests,
            'survey_responds': survey_responds,
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
        member = Member.objects.get(pk=pk)

        print("이 친구를 지우는 거..! ")
        print(member)
        # member.delete()
        return render(request, 'index.html')
