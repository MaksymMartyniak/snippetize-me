from django.contrib import admin
from .models import (
    ProgrammingLanguage, Framework, Option, Assistant, Thread, Feedback
)


@admin.register(ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Framework)
class FrameworkAdmin(admin.ModelAdmin):
    list_display = ["name", "get_language"]

    @admin.display(description='language')
    def get_language(self, obj):
        return obj.language.name


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ["name", "option_type", "get_language", "get_framework"]

    @admin.display(description='language')
    def get_language(self, obj):
        return obj.language.name

    @admin.display(description='framework')
    def get_framework(self, obj):
        return obj.framework.name if obj.framework else None


@admin.register(Assistant)
class AssistantAdmin(admin.ModelAdmin):
    list_display = ["name", "get_language", "get_framework", "get_option"]

    @admin.display(description='language')
    def get_language(self, obj):
        return obj.language.name

    @admin.display(description='framework')
    def get_framework(self, obj):
        return obj.framework.name if obj.framework else None

    @admin.display(description='option')
    def get_option(self, obj):
        return obj.option.name if obj.option else None


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "title"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'thread', 'value']
