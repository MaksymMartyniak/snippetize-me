from django.db import models


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
