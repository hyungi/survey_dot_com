from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from draft.forms import DraftForm
from draft.models import Draft, DraftProduce, DraftInterest
from member.models import Member


# draft.views.py


@login_required
def new_draft(request):
    if request.method == "POST":
        form = DraftForm(request.POST)
        if form.is_valid():
            draft = form.save(commit=False)
            member = Member.objects.get(pk=request.user.id)
            draft.member_id = request.user.id
            draft.save()
            DraftProduce.objects.create(draft=draft, member=member)

            return redirect('my_draft', pk=draft.pk)

    else:
        form = DraftForm()

    return render(request, 'draft/draft_edit.html', {'form': form})


@login_required
def edit_draft(request, pk):
    draft = get_object_or_404(Draft, pk=pk)
    if request.method == "POST":
        form = DraftForm(request.POST, instance=draft)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.recent_edit_date = timezone.now()
            draft_produce = DraftProduce.objects.get(draft=draft)
            draft_produce.recent_edit_date = timezone.now()
            draft_produce.save()
            draft.save()
            return redirect('my_draft', pk=draft.pk)

    else:
        form = DraftForm(instance=draft)

    return render(request, 'draft/draft_edit.html', {'form': form})


@login_required
def all_draft_list(request):
    member = Member.objects.get(pk=request.user.id)
    drafts = Draft.objects.all()
    draft_interests = DraftInterest.objects.values('draft').annotate(count=Count('draft')).order_by('-count')
    my_interests = DraftInterest.objects.filter(member=member)
    print(draft_interests.count)
    return render(request, 'draft/all_draft_list.html', {
        'member': member,
        'drafts': drafts,
        'draft_interests': draft_interests,
        'my_interests': my_interests,
    })


@login_required
def my_draft_list(request):
    pk = request.user.id
    member = Member.objects.get(pk=pk)
    drafts = Draft.objects.filter(member_id=member)
    print(drafts)
    return render(request, 'draft/my_draft_list.html', {'drafts': drafts})


@login_required
def my_draft(request, pk):
    draft = Draft.objects.get(pk=pk)
    draft.view_count += 1
    draft.save()
    print(draft)
    return render(request, 'draft/draft_detail.html', {'draft': draft})


@login_required
def del_draft(request, pk):
    member = Member.objects.get(pk=request.user.id)
    draft = Draft.objects.get(pk=pk)
    if draft.member == member:
        draft.delete()

    drafts = Draft.objects.filter(member_id=member)
    return render(request, 'draft/my_draft_list.html', {'drafts': drafts})


@login_required
def interest_draft(request, pk):
    member = Member.objects.get(pk=request.user.id)
    draft = Draft.objects.get(pk=pk)
    if DraftProduce.objects.filter(member=member, draft=draft).count() == 0:
        draft_interest = DraftInterest.objects.filter(member=member, draft=draft)
        if draft_interest.count() == 0:
            DraftInterest.objects.create(member=member, draft=draft)
            print("드래프트에 관심표시!")
            return render(request, 'draft/draft_detail.html', {'draft', draft})
        else:
            draft_interest.delete()
            print("드래프트에 관심 표시 취소!")
            return render(request, 'draft/draft_detail.html', {'draft', draft})

    else:
        print("자기가 만든 드래프트에는 관심 표시 금지!")
        return render(request, 'draft/draft_detail.html', {'draft', draft})


@csrf_protect
@login_required
def search_draft(request):
    if request.method == 'POST':
        query = request.POST['query']
        pk = request.user.id
        member = Member.objects.get(pk=pk)
        drafts = Draft.objects.filter(title__contains=query)
        draft_interests = DraftInterest.objects.select_related('survey').all().annotate(count=Count('survey'))
        return render(request, 'survey/search_result.html', {
            'member': member,
            'drafts': drafts,
            'draft_interests': draft_interests,
        })
