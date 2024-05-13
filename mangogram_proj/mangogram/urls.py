# messages/urls.py
from django.urls import path
from .views import MessageListCreateAPIView

urlpatterns = [
    path('', MessageListCreateAPIView.as_view(), name='message-list-create'),
]
