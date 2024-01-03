from django.urls import path

from .views import (
    PromptOptionsListView, PostPromptView, ListThreadMessagesView,
    ThreadsListView,
)


urlpatterns = [
    path('options/', PromptOptionsListView.as_view(), name='options'),
    path('post-prompt/', PostPromptView.as_view(), name='post-prompt-view'),
    path('thread-messages/', ListThreadMessagesView.as_view(),
         name='thread-messages-view'),
    path('threads-list/', ThreadsListView.as_view(), name='threads-list-view'),
]
