from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Location
from .serializers import GeoResponseSerializer, KnowledgeTextResponseSerializer, KnowledgeNumberResponseSerializer, OpenResponseSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class LocationListView(LoginRequiredMixin, ListView):
    model = Location

class LocationDetailView(LoginRequiredMixin, DetailView):
    model = Location

class GeoProblemView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = GeoResponseSerializer(data = request.data, context = {'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        m = serializer.save()
        return Response({'status': m.correct}, status=status.HTTP_201_CREATED)

class KnowledgeTextProblemView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = KnowledgeTextResponseSerializer(data = request.data, context = {'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        m = serializer.save()
        return Response({'status': m.correct}, status=status.HTTP_201_CREATED)

class KnowledgeNumberProblemView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = KnowledgeNumberResponseSerializer(data = request.data, context = {'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        m = serializer.save()
        return Response({'status': m.correct}, status=status.HTTP_201_CREATED)

class OpenProblemView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = OpenResponseSerializer(data = request.data, context = {'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        m = serializer.save()
        return Response({'status': m.correct}, status=status.HTTP_201_CREATED)