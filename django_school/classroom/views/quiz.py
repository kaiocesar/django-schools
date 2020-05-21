from rest_framework import viewsets, permissions
from classroom.models import Quiz
from classroom.serializers import QuizSerializer

class QuizViewSets(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
