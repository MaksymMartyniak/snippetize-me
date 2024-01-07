from django.urls import path

from .views import (
    PromptOptionsListView, PostPromptView, ListThreadMessagesView,
    ThreadsListView, GetThreadStatusView, CreateFeedback
)


urlpatterns = [
    path('options/', PromptOptionsListView.as_view(), name='options'),
    path('post-prompt/', PostPromptView.as_view(), name='post-prompt-view'),
    path('post-feedback/', CreateFeedback.as_view(), name='post-feedback-view'),
    path('thread-messages/', ListThreadMessagesView.as_view(),
         name='thread-messages-view'),
    path('threads-list/', ThreadsListView.as_view(), name='threads-list-view'),
    path('thread-status/', GetThreadStatusView.as_view(),
         name='thread-status-view'),
]
