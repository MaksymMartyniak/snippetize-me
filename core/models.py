from django.db import models

from users.models import User

from openai import OpenAI
from core.code_generation_utils.communicators import OpenAICommunicator


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Framework(models.Model):
    name = models.CharField(max_length=128)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.language} {self.name}"


class Option(models.Model):
    """Model for representing library, package, framework and their parts"""
    OPTIONS = (
        ('FRAME', 'Framework'),  # in this case framework can't be null
        ('LIB', 'Library'),
        ('PACK', 'Package'),
        ('D_P', 'Design Pattern'),
    )
    name = models.CharField(max_length=128)
    option_type = models.CharField(max_length=5, choices=OPTIONS)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    framework = models.ForeignKey(
        Framework, null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.language} {self.framework} {self.name}"


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    open_ai_thread_id = models.CharField(max_length=256, null=True, blank=True)
    open_ai_run_id = models.CharField(max_length=256, null=True, blank=True)

    def get_status(self, client: OpenAI):
        run = client.beta.threads.runs.retrieve(
            thread_id=self.open_ai_thread_id,
            run_id=self.open_ai_run_id,
        )
        return run.status

    def get_msgs(self, client: OpenAI):
        messages = client.beta.threads.messages.list(
            thread_id=self.open_ai_thread_id
        )
        return messages


class Prompt(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    framework = models.ForeignKey(
        Framework, null=True, blank=True, on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        Option, null=True, blank=True, on_delete=models.CASCADE
    )
    # limited to the CharField due to the openai api tokens limit per min
    # 1 word eq around 2 tokens
    # the prompt will contain around 320 words = 640 tokens
    # TPM (tokens per min) = 10 000 -> 15 prompts (requests)
    prompt_text = models.CharField(max_length=2048)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Response(models.Model):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    original_text = models.TextField(blank=True, null=True)
    first_snippet = models.TextField(blank=True, null=True)
    second_snippet = models.TextField(blank=True, null=True)
    comparison_text = models.TextField(blank=True, null=True)
    api_response_id = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResponseStatus(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    status = models.IntegerField()
    err_msg = models.TextField()  # maybe this should be JSON


class Assistant(models.Model):
    assistant_id = models.CharField(max_length=256, blank=True, null=True)  # open ai api id
    name = models.CharField(max_length=128)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)
    framework = models.ForeignKey(
        Framework, null=True, blank=True, on_delete=models.CASCADE
    )
    option = models.ForeignKey(
        Option, null=True, blank=True, on_delete=models.CASCADE
    )
    instruction = models.TextField()
    model = models.CharField(max_length=256, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Check if it's a new instance
        if self._state.adding:
            # Your code to create an OpenAI assistant
            communicator = OpenAICommunicator()
            client: OpenAI = communicator.api_client
            assistant = communicator.api_client.beta.assistants.create(
                # Customize the name and instructions as needed
                name=f"{self.name} Assistant",
                instructions=self.instruction,
                model='gpt-4-1106-preview',
                tools=[{"type": "code_interpreter"}],
            )

            # Optionally, store the OpenAI assistant ID or other details in the model
            self.assistant_id = assistant.id  # Assuming 'id' is the attribute for the assistant's ID

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
