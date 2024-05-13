# messages/views.py
import datetime
from rest_framework import generics
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.utils import timezone
class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        timestamp = self.request.query_params.get('timestamp', None)
        if timestamp:
            messages = Message.objects.filter(timestamp__gte=timestamp)
        else:
            messages = Message.objects.all()
        return messages

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
