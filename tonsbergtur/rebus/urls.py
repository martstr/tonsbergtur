from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import LocationListView, LocationDetailView, GeoProblemView, KnowledgeTextProblemView, KnowledgeNumberProblemView, OpenProblemView

app_name = 'rebus'
urlpatterns = [
    path('', views.index, name='index'),
    path('location/', LocationListView.as_view(), name='location-list'),
    path('location/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('check-location/', GeoProblemView.as_view(), name='check-location'),
    path('check-text/', KnowledgeTextProblemView.as_view(), name='check-text'),
    path('check-number/', KnowledgeNumberProblemView.as_view(), name='check-number'),
    path('check-open/', OpenProblemView.as_view(), name='check-open')
]

urlpatterns = format_suffix_patterns(urlpatterns)