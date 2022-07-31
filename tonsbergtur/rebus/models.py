from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from geopy.distance import distance as geo_distance
from Levenshtein import distance as levenshtein_distance

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Location(models.Model):
    title = models.CharField(
            max_length = 50,
        )
    hidden_title = models.CharField(
            max_length = 50
        )
    description = RichTextUploadingField()

    def __str__(self):
        return self.title

    def get_title(self):
        # Utvid denne til å sjekke om man kan vise hidden_title i stedet
        return self.title

    def get_problem_count(self):
        return self.geoproblem_set.count() + self.knowledgetextproblem_set.count() + self.knowledgenumberproblem_set.count()

class Problem(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(
            max_length=50,
        )
    description = RichTextUploadingField()
    location = models.ForeignKey(Location, on_delete = models.CASCADE)
    
    def verify_answer(self) -> bool:
        raise NotImplementedError

    def __str__(self):
        return self.title

class Response(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    correct = models.BooleanField(default = False)

class GeoProblem(Problem):
    latitude = models.FloatField()
    longitude = models.FloatField()
    threshold = models.IntegerField(default=25, help_text='Accepted distance in meters from point')

    def verify_answer(self, submitted_latitude: float, submitted_longitude: float) -> bool:
        d = geo_distance((self.latitude, self.longitude), (submitted_latitude, submitted_longitude)).m
        return d <= self.threshold

class GeoResponse(Response):
    problem = models.ForeignKey(GeoProblem, on_delete = models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

class KnowledgeTextProblem(Problem):
    correct_answer = models.CharField(max_length = 100)
    threshold = models.IntegerField(default=0, help_text='Accepted Levenshtein distance between given and correct answer. 0 for only exact answers')

    def verify_answer(self, submitted_answer: str) -> bool:
        d = levenshtein_distance(self.correct_answer.lower(), submitted_answer.lower())
        return (d <= self.threshold)

class KnowledgeTextResponse(Response):
    problem = models.ForeignKey(KnowledgeTextProblem, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 100)

class KnowledgeNumberProblem(Problem):
    correct_answer = models.FloatField()
    threshold = models.IntegerField(default=0, help_text='Accepted distance from correct answer, in percent. If correct_answer is 0, the distance is treated as if it was 1')

    def verify_answer(self, submitted_answer: float) -> bool:
        if self.correct_answer == 0:
            ratio = 1
        else:
            ratio = self.correct_answer
        d = 100*abs(submitted_answer - self.correct_answer)/ratio
        return (d <= self.threshold)
    
class KnowledgeNumberResponse(Response):
    problem = models.ForeignKey(KnowledgeNumberProblem, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 100)

class OpenProblem(Problem):

    def verify_answer(self):
        return True

class OpenResponse(Response):
    problem = models.ForeignKey(OpenProblem, on_delete = models.CASCADE)

## TODO
#
# - Innlogging og brukertilpassing
# - Sjekk om det finnes riktige svar
# - Vise skjema for hver iterasjon
# - Lokasjoner med ålreit formatering
# X Oppgaver på lokasjon
# X GPS-innsending
#   X Avstand mellom to punkter
# - Sette lagnavn for bruker