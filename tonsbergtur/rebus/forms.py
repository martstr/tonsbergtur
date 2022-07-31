from django import forms
from .models import GeoProblem, KnowledgeTextProblem, KnowledgeNumberProblem, OpenProblem

class ProblemForm(forms.Form):
    pass

class GeoProblemForm(ProblemForm):
    problem = GeoProblem
    longitude = forms.FloatField(widget=forms.HiddenInput())
    latitude = forms.FloatField(widget=forms.HiddenInput())

class KnowledgeTextProblemForm(ProblemForm):
    submitted_answer = forms.CharField(label='Deres supergeniale svar', max_length=100)

class KnowledgeNumberProblemForm(ProblemForm):
    submitted_answer = forms.FloatField(label='Deres supergeniale svar')

class OpenProblemForm(ProblemForm):
    pass