from rest_framework.serializers import Serializer, ModelSerializer, CharField

from .models import (ProgrammingLanguage, Framework, Option, Thread)


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


class ThreadMessageSerializer(Serializer):
    role = CharField()
    content = CharField()

    @staticmethod
    def parse_data(thread_messages) -> list[dict]:
        parsed_msgs = []
        for msg in thread_messages.data:
            parsed_msgs.append({
                "role": msg.role,
                "content": msg.content[0].text.value
            })
        parsed_msgs.reverse()
        return parsed_msgs


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = ('id', 'user', 'title', 'updated_at')
