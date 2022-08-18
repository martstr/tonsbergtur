from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationListView, LocationDetailView, GeoProblemView, KnowledgeTextProblemView, KnowledgeNumberProblemView, OpenProblemView, TeamNameView, ResultView

app_name = 'rebus'
urlpatterns = [
    path('location/', LocationListView.as_view(), name='location-list'),
    path('location/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('check-location/', GeoProblemView.as_view(), name='check-location'),
    path('check-text/', KnowledgeTextProblemView.as_view(), name='check-text'),
    path('check-number/', KnowledgeNumberProblemView.as_view(), name='check-number'),
    path('check-open/', OpenProblemView.as_view(), name='check-open'),
    path('set-team-name/', TeamNameView.as_view(), name='set-team-name'),
    path('results/', ResultView.as_view(), name='results'),
]

urlpatterns = format_suffix_patterns(urlpatterns)