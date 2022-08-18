from django.http import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Value, ExpressionWrapper
from django.db import models

from .models import Location, ExtendedUser, GeoProblem, KnowledgeTextProblem, KnowledgeNumberProblem, OpenProblem, GeoResponse, KnowledgeTextResponse, KnowledgeNumberResponse, OpenResponse
from .serializers import GeoResponseSerializer, KnowledgeTextResponseSerializer, KnowledgeNumberResponseSerializer, OpenResponseSerializer, TeamNameSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

class TeamNameView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        serializer = TeamNameSerializer(user.extendeduser, data = request.data, context = {'user': request.user}, partial=True)
        serializer.is_valid(raise_exception=True)
        m = serializer.save()
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

class ResultView(TemplateView):
    model = ExtendedUser
    template_name = 'rebus/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        geoproblems =    GeoProblem.objects.values('id', 'title', 'location', 'location__title').annotate(type=ExpressionWrapper(Value('1geo'), output_field=models.CharField(max_length=20)))
        textproblems =   KnowledgeTextProblem.objects.values('id', 'title', 'location', 'location__title').annotate(type=ExpressionWrapper(Value('2text'), output_field=models.CharField(max_length=20)))
        numberproblems = KnowledgeNumberProblem.objects.values('id', 'title', 'location', 'location__title').annotate(type=ExpressionWrapper(Value('3number'), output_field=models.CharField(max_length=20)))
        openproblems =   OpenProblem.objects.values('id', 'title', 'location', 'location__title').annotate(type=ExpressionWrapper(Value('4open'), output_field=models.CharField(max_length=20)))

        problems = geoproblems.union(textproblems).union(numberproblems).union(openproblems).order_by('location', 'type')

        georesponses =    GeoResponse.objects.values('user_id', 'problem_id').filter(correct=True).annotate(type=ExpressionWrapper(Value('1geo'), output_field=models.CharField(max_length=20))).distinct()
        textresponses =   KnowledgeTextResponse.objects.values('user_id', 'problem_id').filter(correct=True).annotate(type=ExpressionWrapper(Value('2text'), output_field=models.CharField(max_length=20))).distinct()
        numberresponses = KnowledgeNumberResponse.objects.values('user_id', 'problem_id').filter(correct=True).annotate(type=ExpressionWrapper(Value('3number'), output_field=models.CharField(max_length=20))).distinct()
        openresponses =   OpenResponse.objects.values('user_id', 'problem_id').filter(correct=True).annotate(type=ExpressionWrapper(Value('4open'), output_field=models.CharField(max_length=20))).distinct()

        responses = georesponses.union(textresponses).union(numberresponses).union(openresponses)
        responses = list(responses)

        users = ExtendedUser.objects.filter(player=True)

        results = []
        total = [0 for i in users]

        for problem in problems:
            result = [problem['location__title'], problem['title']] + [5*({'user_id': user.id, 'problem_id': problem['id'], 'type': problem['type']} in responses) for user in users]
            for i in range(len(users)):
                total[i] = total[i] + result[i+2]
            results.append(result)

        context['results'] = results
        context['users'] = users
        context['total'] = total

        return context