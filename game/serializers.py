from rest_framework import serializers
from .models import Question, CustomQuestion, CoupleSession

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'mode']

class CustomQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuestion
        fields = '__all__'
        
        couple = serializers.PrimaryKeyRelatedField(queryset=CoupleSession.objects.all())

class CoupleSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoupleSession
        fields = ['id', 'secret_word', 'partner1_name', 'partner2_name']
