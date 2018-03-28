from django import forms
from .models import Member


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ('name', 'nick_name', 'birth', 'company', 'major', 'email')
