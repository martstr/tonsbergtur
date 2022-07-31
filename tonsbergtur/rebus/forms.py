from django import forms
from .models import Problem, Response, GeoProblem, GeoResponse, KnowledgeTextProblem, KnowledgeTextResponse, KnowledgeNumberProblem, KnowledgeNumberResponse, OpenProblem, OpenResponse

class ProblemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProblemForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Response
        exclude = ['user', 'problem', 'correct']

    def save(self, commit=True, *args, **kwargs):
        m = super(ProblemForm, self).save(commit=False, *args, **kwargs)
        m.user = self.user
        if commit:
            m.save()
        return m

class GeoProblemForm(ProblemForm):
    class Meta(ProblemForm.Meta):
        model = GeoResponse
        widgets = {
                'longitude': forms.HiddenInput(),
                'latitude': forms.HiddenInput()
            }

    def save(self, commit=True, *args, **kwargs):
        m = super(GeoProblemForm, self).save(commit=False, *args, **kwargs)
        m.correct = m.problem.verify_answer(m.latitude, m.longitude)
        if commit:
            m.save()
        return m

class KnowledgeTextProblemForm(ProblemForm):
    class Meta(ProblemForm.Meta):
        model = KnowledgeTextResponse

    def save(self, commit=True, *args, **kwargs):
        m = super(GeoProblemForm, self).save(commit=False, *args, **kwargs)
        m.correct = m.problem.verify_answer(m.answer)
        if commit:
            m.save()
        return m

class KnowledgeNumberProblemForm(ProblemForm):
    class Meta(ProblemForm.Meta):
        model = KnowledgeNumberResponse

    def save(self, commit=True, *args, **kwargs):
        m = super(GeoProblemForm, self).save(commit=False, *args, **kwargs)
        m.correct = m.problem.verify_answer(m.answer)
        if commit:
            m.save()
        return m

class OpenProblemForm(ProblemForm):
    class Meta(ProblemForm.Meta):
        model = OpenResponse

    def save(self, commit=True, *args, **kwargs):
        m = super(GeoProblemForm, self).save(commit=False, *args, **kwargs)
        m.correct = m.problem.verify_answer()
        if commit:
            m.save()
        return m