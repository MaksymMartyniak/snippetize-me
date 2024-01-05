from openai import OpenAI
from typing import Optional
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ProgrammingLanguage, Thread, Assistant
from .code_generation_utils.communicators import OpenAICommunicator
from .serializers import (
    ProgrammingLanguageSerializer, ThreadMessageSerializer,
    ThreadSerializer,
)

communicator = OpenAICommunicator()
client: OpenAI = communicator.api_client


class PromptOptionsListView(ListAPIView):
    serializer_class = ProgrammingLanguageSerializer
    queryset = ProgrammingLanguage.objects.all()


class PostPromptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # Extract input parameters from request.data
        thread_id = request.data.get('thread_id')
        programming_language_id = request.data.get('programming_language_id')
        framework_id = request.data.get('framework_id')
        option_id = request.data.get('option_id')
        prompt = request.data.get('prompt')

        # Extract query parameter
        res_type = request.query_params.get('res_type')
        thread = self.invoke_thread(thread_id)
        run = self.invoke_run(
            thread, prompt, programming_language_id, framework_id,
            option_id
        )
        # Return response
        return Response({
            "message": f"Your prompt has status 'f{run.status}'. "
                       f"It will be processed as soon as possible.",
            "thread_id": thread.id
        })

    def invoke_thread(self, thread_id: Optional[int]) -> Thread:
        if thread_id is None:
            open_ai_thread = client.beta.threads.create()
            thread = Thread(
                user=self.request.user,
                open_ai_thread_id=open_ai_thread.id,
            )
            thread.save()
        else:
            thread = Thread.objects.get(id=thread_id)
        return thread

    @staticmethod
    def invoke_run(
            thread: Thread,
            prompt: str,
            language_id: int,
            framework_id: Optional[int],
            option_id: Optional[int]
    ):
        message = client.beta.threads.messages.create(
            thread_id=thread.open_ai_thread_id,
            role='user',
            content=prompt,
        )
        assistant = Assistant.objects.get(
            language_id=language_id,
            framework_id=framework_id,
            option_id=option_id,
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.open_ai_thread_id,
            assistant_id=assistant.assistant_id
        )
        thread.open_ai_run_id = run.id
        thread.save()
        return run


class GetThreadStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Extract query parameters
        thread_id = request.query_params.get('thread_id')

        try:
            thread = Thread.objects.get(id=thread_id)
        except Thread.DoesNotExist as exc:
            return Response({
                "exc": exc, "user": self.request.user.id,
                "thread_id": thread_id
            })
        return Response({"status": thread.get_status(client)})


class ListThreadMessagesView(APIView):
    def get(self, request, format=None):
        thread = Thread.objects.get(id=request.data.get('thread_id'))
        thread_msgs = thread.get_msgs(client)

        # Serialize the data
        serializer = ThreadMessageSerializer()
        processed_data = serializer.parse_data(thread_msgs)
        serializer = ThreadMessageSerializer(data=processed_data, many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


class ThreadsListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ThreadSerializer

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(user=user).order_by('-updated_at')
