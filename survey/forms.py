from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ('title', 'summary', 'content', 'start_date', 'end_date', 'survey_image')

# class GroupForm(forms.ModelForm):
#
#     class Meta:
#         model = Group
#         fields = ('group_name', 'group_project', 'group_goal', 'start_date', 'end_date')
#
