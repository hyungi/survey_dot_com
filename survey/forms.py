from django import forms
from .models import Survey


class SurveyForm(forms.ModelForm):

    class Meta:
        model = Survey
        fields = ('title', 'summary', 'content', 'start_date', 'end_date', 'form_link', 'survey_image')
