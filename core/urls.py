from django.urls import path

from .views import PromptOptionsListView


urlpatterns = [
    path('options/', PromptOptionsListView.as_view(), name='options'),
]
