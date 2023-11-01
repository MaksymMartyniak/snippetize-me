from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import ProgrammingLanguage
from .serializers import ProgrammingLanguageSerializer


class PromptOptionsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()
