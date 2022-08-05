from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from geopy.distance import distance as geo_distance
from Levenshtein import distance as levenshtein_distance

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

    def get_problem_count(self) -> int:
        return self.geoproblem_set.count() + \
            self.knowledgetextproblem_set.count() + \
            self.knowledgenumberproblem_set.count() + \
            self.openproblem_set.count()

    def get_completed_problem_count(self, user: User) -> int:
        return \
            GeoResponse.objects.values("problem")\
            .filter(problem__location = self, user=user, correct = True)\
            .distinct().count()\
          + KnowledgeTextResponse.objects.values("problem")\
            .filter(problem__location = self, user=user, correct = True)\
            .distinct().count()\
          + KnowledgeNumberResponse.objects.values("problem")\
            .filter(problem__location = self, user=user, correct = True)\
            .distinct().count()\
          + OpenResponse.objects.values("problem")\
            .filter(problem__location = self, user=user, correct = True)\
            .distinct().count()

    def location_completed(self, user: User) -> bool:
        return (self.get_problem_count() == self.get_completed_problem_count(user))

    def location_found(self, user: User) -> bool:
        if self.geoproblem_set.exists():
            if not GeoResponse.objects.filter(problem__location = self, user = user, correct = True).exists():
                return self.title
        return self.hidden_title


class Problem(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(
            max_length=50,
        )
    description = RichTextUploadingField()
    location = models.ForeignKey(Location, on_delete = models.CASCADE)

    def user_has_correct_answer(self, user: User) -> bool:
        raise NotImplementedError
    
    def verify_answer(self) -> bool:
        raise NotImplementedError

    def __str__(self):
        return self.title

class Response(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    correct = models.BooleanField(default = False)

class GeoProblem(Problem):
    latitude = models.FloatField()
    longitude = models.FloatField()
    threshold = models.IntegerField(default=25, help_text='Accepted distance in meters from point')

    def user_has_correct_answer(self, user: User) -> bool:
        return GeoResponse.objects.filter(problem = self, user = user, correct = True).exists()

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
    
    def get_accepted_answer(self, user):
        if self.user_has_correct_answer(user):
            return KnowledgeTextResponse.objects.filter(problem = self, user = user, correct = True).last().answer

    def user_has_correct_answer(self, user: User) -> bool:
        return KnowledgeTextResponse.objects.filter(problem = self, user = user, correct = True).exists()

    def verify_answer(self, submitted_answer: str) -> bool:
        d = levenshtein_distance(self.correct_answer.lower(), submitted_answer.lower())
        return (d <= self.threshold)

class KnowledgeTextResponse(Response):
    problem = models.ForeignKey(KnowledgeTextProblem, on_delete = models.CASCADE)
    answer = models.CharField(max_length = 100)

class KnowledgeNumberProblem(Problem):
    correct_answer = models.FloatField()
    threshold = models.IntegerField(default=0, help_text='Accepted distance from correct answer, in percent. If correct_answer is 0, the distance is treated as if it was 1')
       
    def get_accepted_answer(self, user):
        if self.user_has_correct_answer(user):
            return KnowledgeNumberResponse.objects.filter(problem = self, user = user, correct = True).last().answer

    def user_has_correct_answer(self, user: User) -> bool:
        return KnowledgeNumberResponse.objects.filter(problem = self, user = user, correct = True).exists()

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

    def user_has_correct_answer(self, user: User) -> bool:
        return OpenResponse.objects.filter(problem = self, user = user, correct = True).exists()

    def verify_answer(self):
        return True

class OpenResponse(Response):
    problem = models.ForeignKey(OpenProblem, on_delete = models.CASCADE)

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    team_name = models.CharField(max_length = 100)

## TODO
#
# - Skjul form for korrekt besvarte spørsmål
# - Lokasjoner med ålreit formatering
# X Lagnavn i head title
# X Templatetag for å vise get_title dersom det er løst en geo-oppgave
# X Sette lagnavn for bruker
#   X JS-kdoe for å sette lagnavnet
# X Fjerne CORS?
# X Innlogging og krav om ditto
# X Brukertilpassing
# X Sjekk om det finnes riktige svar
# X Vise skjema for hver iterasjon
#   X Javascript for nevnte
# X Oppgaver på lokasjon
# X GPS-innsending
#   X Avstand mellom to punkter
# X Riktig bruk av index