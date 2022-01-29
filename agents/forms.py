from django import forms
from leads.models import Agent


class AgentModelFrom(forms.ModelForm):
    class Meta:
        model = Agent
        fields = (
            'user',
        )
