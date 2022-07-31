from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location
from .forms import ProblemForm, GeoProblemForm, KnowledgeTextProblemForm, KnowledgeNumberProblemForm, OpenProblemForm
from .serializers import CoordinateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from geopy.distance import distance

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class LocationListView(ListView):
    model = Location

class LocationDetailView(DetailView):
    model = Location

class ResponseView(FormView):
    template_name = 'response.html'
    form_class = ProblemForm
    success_url = '/todo2/'

    def get_form_kwargs(self):
        kwargs = super(ResponseView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class GeoResponseView(ResponseView):
    form_class = GeoProblemForm

class KnowledgeTextResponseView(ResponseView):
    form_class = KnowledgeTextProblemForm
    
class KnowledgeNumberResponseView(ResponseView):
    form_class = KnowledgeNumberProblemForm
    
class OpenResponseView(ResponseView):
    form_class = OpenProblemForm

class CheckLocationView(APIView):
    permission_classes = ()
    authentication_classes = ()
    LONG1 = 13.404954
    LAT1 = 52.520007

    def post(self, request, format=None):
        serializer = CoordinateSerializer(data = request.data)
        if serializer.is_valid():
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']
            d = distance((self.LAT1, self.LONG1), (latitude, longitude)).m 
            if d < 25:
                return Response({'status': True, 'dist': d})
            else:
                return Response({'status': False, 'dist': d})
            # 

        return Response({'status': False}, status=status.HTTP_400_BAD_REQUEST)

#class GeoProblemView(LoginRequiredMixin, FormView):
#    template_name='todo.html'
#    form_class = GeoProblemForm
#    success_url = 'todo/'
   
#    def form_valid(self, form):
#        if 