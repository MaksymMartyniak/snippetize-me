from rest_framework.serializers import Serializer, ModelSerializer

from .models import (ProgrammingLanguage, Framework, Option)


class FrameworkSerializer(ModelSerializer):
    class Meta:
        model = Framework
        fields = ('id', 'name')


class OptionSerializer(ModelSerializer):
    class Meta:
        model = Option
        fields = ('id', 'name', 'option_type', 'framework')


class ProgrammingLanguageSerializer(ModelSerializer):
    frameworks = FrameworkSerializer(source='framework_set', many=True)
    options = OptionSerializer(source='option_set', many=True)

    class Meta:
        model = ProgrammingLanguage
        fields = ('id', 'name', 'frameworks', 'options')
