from django.urls import path

from .views import PromptOptionsListView, PostPromptView, ListThreadMessagesView


urlpatterns = [
    path('options/', PromptOptionsListView.as_view(), name='options'),
    path('post-prompt/', PostPromptView.as_view(), name='post-prompt-view'),
    path('thread-messages/', ListThreadMessagesView.as_view(),
         name='thread-messages-view'),
]
