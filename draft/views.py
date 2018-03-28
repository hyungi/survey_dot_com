from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from draft.forms import DraftForm
from draft.models import Draft, DraftProduce
from member.models import Member
# draft.views.py


def new_draft(request):
    if request.user.is_authenticated:
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


def edit_draft(request, pk):
    if request.user.is_authenticated:
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


def my_draft_list(request):
    if request.user.is_authenticated:
        pk = request.user.id
        member = Member.objects.get(pk=pk)
        drafts = Draft.objects.filter(member_id=member).order_by('-draft_date')
        print(drafts)
        return render(request, 'draft/my_draft_list.html', {'drafts': drafts})


def my_draft(request, pk):
    if request.user.is_authenticated:
        draft = Draft.objects.get(pk=pk)
        draft.view_count += 1
        draft.save()
        print(draft)
        return render(request, 'draft/draft_detail.html', {'draft': draft})


def del_draft(request, pk):
    if request.user.is_authenticated:
        member = Member.objects.get(pk=request.user.id)
        draft = Draft.objects.get(pk=pk)
        if draft.member == member:
            draft.delete()

        drafts = Draft.objects.filter(member_id=member)
        return render(request, 'draft/my_draft_list.html', {'drafts': drafts})
