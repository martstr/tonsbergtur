
from rest_framework import serializers

from .models import Response, GeoResponse, KnowledgeTextResponse, KnowledgeNumberResponse, OpenResponse
from .models import Problem,  GeoProblem,  KnowledgeTextProblem,  KnowledgeNumberProblem,  OpenProblem

class ResponseSerializer(serializers.ModelSerializer):
    problem_id = serializers.IntegerField()

    class Meta:
        model = Response
        exclude = ['user', 'correct', 'created_at']
        read_only_fields = ['problem_id']

    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super(ResponseSerializer, self).create(validated_data)

class GeoResponseSerializer(ResponseSerializer):
    class Meta(ResponseSerializer.Meta):
        model = GeoResponse

    def create(self, validated_data):
        validated_data['problem'] = GeoProblem.objects.get(pk=validated_data['problem_id'])
        validated_data['correct'] = validated_data['problem'].verify_answer(validated_data['latitude'], validated_data['longitude'])

        return super(GeoResponseSerializer, self).create(validated_data)

class KnowledgeTextResponseSerializer(ResponseSerializer):
    class Meta(ResponseSerializer.Meta):
        model = KnowledgeTextResponse

    def create(self, validated_data):
        validated_data['problem'] = KnowledgeTextProblem.objects.get(pk=validated_data['problem_id'])
        validated_data['correct'] = validated_data['problem'].verify_answer(validated_data['answer'])

        return super(KnowledgeTextResponseSerializer, self).create(validated_data)

class KnowledgeNumberResponseSerializer(ResponseSerializer):
    class Meta(ResponseSerializer.Meta):
        model = KnowledgeNumberResponse

    def create(self, validated_data):
        validated_data['problem'] = KnowledgeNumberProblem.objects.get(pk=validated_data['problem_id'])
        validated_data['correct'] = validated_data['problem'].verify_answer(float(validated_data['answer']))

        return super(KnowledgeNumberResponseSerializer, self).create(validated_data)

class OpenResponseSerializer(ResponseSerializer):
    class Meta(ResponseSerializer.Meta):
        model = OpenResponse

    def create(self, validated_data):
        validated_data['problem'] = OpenProblem.objects.get(pk=validated_data['problem_id'])
        validated_data['correct'] = validated_data['problem'].verify_answer()

        return super(OpenResponseSerializer, self).create(validated_data)
