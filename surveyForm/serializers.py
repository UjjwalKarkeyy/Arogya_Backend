from rest_framework import serializers
from .models import Survey, Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # Expose key fields; survey will be set by parent serializer on create
        fields = (
            'id',
            'title',
            'description',
            'question_type',
            'required',
        )


class SurveySerializer(serializers.ModelSerializer):
    # include questions inside survey
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Survey
        fields = 'all'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        survey = Survey.objects.create(validated_data)
        for q in questions_data:
            Question.objects.create(survey=survey)
        return survey

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)

        # Update survey fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If questions provided, replace existing questions with new set
        if questions_data is not None:
            instance.questions.all().delete()
            for q in questions_data:
                Question.objects.create(survey=instance, **q)

        return instance