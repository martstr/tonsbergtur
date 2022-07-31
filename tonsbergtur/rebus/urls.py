from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from .views import LocationListView, LocationDetailView, CheckLocationView

app_name = 'rebus'
urlpatterns = [
    path('', views.index, name='index'),
    path('location/', LocationListView.as_view(), name='location-list'),
    path('location/<int:pk>/', LocationDetailView.as_view(), name='location-detail'),
    path('check-location/', CheckLocationView.as_view(), name='check-location')
]

urlpatterns = format_suffix_patterns(urlpatterns)