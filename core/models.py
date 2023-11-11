from django.db import models

from users.models import User


class ProgrammingLanguage(models.Model):
    name = models.CharField(max_length=64)


class Framework(models.Model):
    name = models.CharField(max_length=128)
    language = models.ForeignKey(ProgrammingLanguage, on_delete=models.CASCADE)


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


class Thread(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
